import secrets
import bcrypt
import transaction
from datetime import datetime
from functools import wraps

from rest_framework import permissions, status as http
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .zodb_client import get_db
from .models import (
    Users, Status, EventTypes, Discounts, TicketTypes, Events, Orders,
    Tickets, Messages, Notifications, Token
)
from .serializers import (
    StatusSerializer, EventTypesSerializer, DiscountsSerializer,
    TicketTypesSerializer, EventsSerializer, OrdersSerializer,
    TicketsSerializer, MessagesSerializer, NotificationsSerializer
)

class ZODBUser:
    def __init__(self, user_obj):
        self.obj = user_obj
        self.id = user_obj.id
        self.email = user_obj.email
        self.is_active = user_obj.is_active
        self.is_staff = getattr(user_obj, 'is_admin', False)
        self.is_authenticated = True

class ZODBTokenAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth = get_authorization_header(request).decode("utf-8")
        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        key = parts[1].strip()
        
        db = get_db()
        conn = db.open()
        try:
            root = conn.root()
            tokens = root.get('tokens')
            if not tokens or key not in tokens:
                raise AuthenticationFailed("Invalid token.")
            
            token_obj = tokens[key]
            user_obj = token_obj.user
            
            if not user_obj.is_active:
                raise AuthenticationFailed("User inactive.")
            pass 
        finally:
            conn.close()
        return (ZODBUser(user_obj), key)

def with_zodb(view_method):
    @wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        self.db = get_db()
        self.conn = self.db.open()
        self.root = self.conn.root()
        try:
            if request.user and request.user.is_authenticated:
                users = self.root['users']
                if request.user.id in users:
                    self.current_user = users[request.user.id]
                else:
                    self.current_user = None
            else:
                self.current_user = None
                
            return view_method(self, request, *args, **kwargs)
        except Exception as e:
            transaction.abort()
            raise e
        finally:
            self.conn.close()
    return wrapper

class ZODBView(APIView):
    authentication_classes = [ZODBTokenAuthentication]
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @with_zodb
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")
        name = request.data.get("name", "")
        surname = request.data.get("surname", "")

        if not email or not password:
            return Response({"error": "email and password required"}, status=400)

        for user in self.root['users'].values():
            if user.email == email:
                return Response({"error": "This email is already taken"}, status=400)

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        with transaction.manager:
            new_user = Users(email=email, password_hash=pw_hash, name=name, surname=surname)
            self.root['users'][new_user.id] = new_user
            
            token_key = secrets.token_hex(20)
            new_token = Token(key=token_key, user=new_user)
            self.root['tokens'][token_key] = new_token
        
        return Response({
            "success": True, 
            "token": token_key, 
            "user": {
                "id": new_user.id, 
                "email": email,
                "is_staff": new_user.is_admin
            }
        }, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @with_zodb
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")

        user = None
        for u in self.root['users'].values():
            if u.email == email:
                user = u
                break
        
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return Response({"error": "Invalid credentials"}, status=400)
            
        if not user.is_active:
             return Response({"error": "Account deactivated"}, status=400)

        with transaction.manager:
            token_key = secrets.token_hex(20)
            new_token = Token(key=token_key, user=user)
            self.root['tokens'][token_key] = new_token

        return Response({
            "token": token_key, 
            "user": {
                "id": user.id, 
                "email": email,
                "is_staff": user.is_admin
            }
        }, status=200)


class StatusListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @with_zodb
    def get(self, request):
        data = [StatusSerializer(s).data for s in self.root['status'].values()]
        return Response(data)

    @with_zodb
    def post(self, request):
        ser = StatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj = Status(name=ser.validated_data['name'])
            self.root['status'][obj.id] = obj
        return Response(StatusSerializer(obj).data, status=201)

class StatusDetailView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @with_zodb
    def get(self, request, pk):
        obj = self.root['status'].get(pk)
        if not obj: return Response(status=404)
        return Response(StatusSerializer(obj).data)
        
    @with_zodb
    def put(self, request, pk):
        obj = self.root['status'].get(pk)
        if not obj: return Response(status=404)
        ser = StatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj.name = ser.validated_data['name']
            obj.updated_at = datetime.now()
        return Response(StatusSerializer(obj).data)

    @with_zodb
    def patch(self, request, pk):
        obj = self.root['status'].get(pk)
        if not obj: return Response(status=404)
        ser = StatusSerializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj.name = ser.validated_data.get('name', obj.name)
            obj.updated_at = datetime.now()
        return Response(StatusSerializer(obj).data)

    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['status']:
            with transaction.manager:
                del self.root['status'][pk]
            return Response(status=204)
        return Response(status=404)


class EventTypeListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @with_zodb
    def get(self, request):
        data = [EventTypesSerializer(s).data for s in self.root['event_types'].values()]
        return Response(data)

    @with_zodb
    def post(self, request):
        ser = EventTypesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj = EventTypes(name=ser.validated_data['name'])
            self.root['event_types'][obj.id] = obj
        return Response(EventTypesSerializer(obj).data, status=201)

class EventTypeDetailView(ZODBView):
    @with_zodb
    def get(self, request, pk):
        obj = self.root['event_types'].get(pk)
        if not obj: return Response(status=404)
        return Response(EventTypesSerializer(obj).data)
    
    @with_zodb
    def put(self, request, pk):
        obj = self.root['event_types'].get(pk)
        if not obj: return Response(status=404)
        ser = EventTypesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj.name = ser.validated_data['name']
            obj.updated_at = datetime.now()
        return Response(EventTypesSerializer(obj).data)

    @with_zodb
    def patch(self, request, pk):
        obj = self.root['event_types'].get(pk)
        if not obj: return Response(status=404)
        ser = EventTypesSerializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            obj.name = ser.validated_data.get('name', obj.name)
            obj.updated_at = datetime.now()
        return Response(EventTypesSerializer(obj).data)
        
    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['event_types']:
            with transaction.manager:
                del self.root['event_types'][pk]
            return Response(status=204)
        return Response(status=404)

class DiscountsListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @with_zodb
    def get(self, request):
        data = [DiscountsSerializer(s).data for s in self.root['discounts'].values()]
        return Response(data)

    @with_zodb
    def post(self, request):
        ser = DiscountsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            obj = Discounts(**d)
            self.root['discounts'][obj.id] = obj
        return Response(DiscountsSerializer(obj).data, status=201)

class DiscountsDetailView(ZODBView):
    @with_zodb
    def get(self, request, pk): # 'id' because lookup_field="id" in original
        obj = self.root['discounts'].get(pk)
        if not obj: return Response(status=404)
        return Response(DiscountsSerializer(obj).data)

    @with_zodb
    def put(self, request, pk):
        obj = self.root['discounts'].get(pk)
        if not obj: return Response(status=404)
        ser = DiscountsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            for k,v in d.items():
                setattr(obj, k, v)
        return Response(DiscountsSerializer(obj).data)

    @with_zodb
    def patch(self, request, pk):
        obj = self.root['discounts'].get(pk)
        if not obj: return Response(status=404)
        ser = DiscountsSerializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            for k,v in d.items():
                setattr(obj, k, v)
        return Response(DiscountsSerializer(obj).data)
        
    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['discounts']:
            with transaction.manager:
                del self.root['discounts'][pk]
            return Response(status=204)
        return Response(status=404)

class TicketTypeListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @with_zodb
    def get(self, request):
        data = [TicketTypesSerializer(s).data for s in self.root['ticket_types'].values()]
        return Response(data)

    @with_zodb
    def post(self, request):
        ser = TicketTypesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            obj = TicketTypes(**d)
            self.root['ticket_types'][obj.id] = obj
        return Response(TicketTypesSerializer(obj).data, status=201)

class TicketTypeDetailView(ZODBView):
    @with_zodb
    def get(self, request, pk):
        obj = self.root['ticket_types'].get(pk)
        if not obj: return Response(status=404)
        return Response(TicketTypesSerializer(obj).data)
        
    @with_zodb
    def put(self, request, pk):
        obj = self.root['ticket_types'].get(pk)
        if not obj: return Response(status=404)
        ser = TicketTypesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            for k,v in d.items():
                setattr(obj, k, v)
        return Response(TicketTypesSerializer(obj).data)

    @with_zodb
    def patch(self, request, pk):
        obj = self.root['ticket_types'].get(pk)
        if not obj: return Response(status=404)
        ser = TicketTypesSerializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with transaction.manager:
            for k,v in d.items():
                setattr(obj, k, v)
        return Response(TicketTypesSerializer(obj).data)

    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['ticket_types']:
            with transaction.manager:
                del self.root['ticket_types'][pk]
            return Response(status=204)
        return Response(status=404)

class EventListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @with_zodb
    def get(self, request):
        data = [EventsSerializer(s).data for s in self.root['events'].values()]
        return Response(data)

    @with_zodb
    def post(self, request):
        ser = EventsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        
        et_id = d.pop('event_type_id', None)
        st_id = d.pop('status_id', None)
        
        if not et_id or not st_id:
             return Response({"error": "event_type_id and status_id are required"}, status=400)

        et = self.root['event_types'].get(et_id)
        st = self.root['status'].get(st_id)
        
        if not et or not st:
            return Response({"error": "Invalid event_type or status ID"}, status=400)
            
        with transaction.manager:
            obj = Events(event_type=et, status=st, **d)
            self.root['events'][obj.id] = obj
        return Response(EventsSerializer(obj).data, status=201)

class EventDetailView(ZODBView):
    @with_zodb
    def get(self, request, pk):
        print(f"DEBUG: EventDetailView GET pk={pk}")
        obj = self.root['events'].get(pk)
        if not obj:
            print(f"DEBUG: Event not found for pk={pk}") 
            return Response(status=404)
        print(f"DEBUG: Event found: {obj.name}")
        return Response(EventsSerializer(obj).data)
        
    @with_zodb
    def put(self, request, pk):
        print(f"DEBUG: EventDetailView PUT pk={pk}")
        return self._update(request, pk, partial=False)

    @with_zodb
    def patch(self, request, pk):
        print(f"DEBUG: EventDetailView PATCH pk={pk}")
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        obj = self.root['events'].get(pk)
        if not obj: return Response(status=404)
        
        ser = EventsSerializer(data=request.data, partial=partial)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        
        et_id = d.pop('event_type_id', None)
        st_id = d.pop('status_id', None)
        
        et = None
        st = None
        if et_id:
            et = self.root['event_types'].get(et_id)
            if not et: return Response({"error": "Invalid event_type_id"}, 400)
        if st_id:
            st = self.root['status'].get(st_id)
            if not st: return Response({"error": "Invalid status_id"}, 400)

        with transaction.manager:
            for k,v in d.items():
                setattr(obj, k, v)
            if et: obj.event_type = et
            if st: obj.status = st
            obj.updated_at = datetime.now()
            
        return Response(EventsSerializer(obj).data)

    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['events']:
            with transaction.manager:
                del self.root['events'][pk]
            return Response(status=204)
        return Response(status=404)

class OrderListCreateView(ZODBView):
    permission_classes = [permissions.IsAuthenticated]

    @with_zodb
    def get(self, request):
        if not self.current_user: return Response([], 200)
        user_orders = []
        for order in self.root['orders'].values():
            if order.user.id == self.current_user.id:
                user_orders.append(order)
        return Response([OrdersSerializer(o).data for o in user_orders])

    @with_zodb
    def post(self, request):
        if not self.current_user:
            return Response({"error": "Auth required"}, status=401)
            
        ser = OrdersSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        
        tickets_data = ser.validated_data.get('tickets_data') or ser.validated_data.get('tickets', [])
        discount_id = ser.validated_data.get('discount_id') or request.data.get('discount')
        
        if discount_id:
            discount_id = str(discount_id)
        
        discount = None
        if discount_id:
            discount = self.root['discounts'].get(discount_id)
            if not discount: return Response({"error": "Invalid discount"}, status=400)
        
        with transaction.manager:
            order = Orders(user=self.current_user, total_price=0, discount=discount)
            order_tickets = []
            final_total = 0.0
            
            for item in tickets_data:
                event_id = str(item.get('event_id') or item.get('event', ''))
                ticket_type_id = str(item.get('ticket_type_id') or item.get('ticket_type', ''))
                qty = item.get('quantity', 1)
                
                ev = self.root['events'].get(event_id)
                tt = self.root['ticket_types'].get(ticket_type_id)
                
                if not ev:
                    transaction.abort()
                    return Response({"error": f"Event not found: {event_id}"}, 400)
                if not tt:
                    transaction.abort()
                    return Response({"error": f"Ticket type not found: {ticket_type_id}"}, 400)
                
                if ev.quantity < qty:
                     transaction.abort()
                     return Response({"error": f"Not enough quantity for {ev.name}"}, 400)
                
                ev.quantity -= qty
                ev._p_changed = True
                
                ticket = Tickets(event=ev, order=order, ticket_type=tt, quantity=qty)
                self.root['tickets'][ticket.id] = ticket
                order_tickets.append(ticket)
                
                price = (float(ev.base_price) * (1 - float(tt.discount))) * qty
                final_total += price

            if discount:
                final_total *= (1 - float(discount.discount_percentage))
            
            order.total_price = final_total
            order.tickets = order_tickets
            self.root['orders'][order.id] = order
            
        return Response(OrdersSerializer(order).data, status=201)

class OrderDetailView(ZODBView):
    permission_classes = [permissions.IsAuthenticated]

    @with_zodb
    def get(self, request, pk):
        order = self.root['orders'].get(pk)
        if not order: return Response(status=404)
        if self.current_user and order.user.id != self.current_user.id:
            return Response(status=404)
        return Response(OrdersSerializer(order).data)

class TicketListCreateView(ZODBView):
    @with_zodb
    def get(self, request):
        return Response([TicketsSerializer(t).data for t in self.root['tickets'].values()])

class TicketDetailView(ZODBView):
    @with_zodb
    def get(self, request, pk):
        ticket = self.root['tickets'].get(pk)
        if not ticket: return Response(status=404)
        return Response(TicketsSerializer(ticket).data)

    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['tickets']:
            with transaction.manager:
                del self.root['tickets'][pk]
            return Response(status=204)
        return Response(status=404)

class MessageListCreateView(ZODBView):
    authentication_classes = [ZODBTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @with_zodb
    def get(self, request):
        if not self.current_user: return Response([])
        msgs = [m for m in self.root['messages'].values() if m.user.id == self.current_user.id]
        return Response([MessagesSerializer(m).data for m in msgs])

    @with_zodb
    def post(self, request):
        ser = MessagesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.manager:
            msg = Messages(user=self.current_user, text=ser.validated_data['text'])
            self.root['messages'][msg.id] = msg
        return Response(MessagesSerializer(msg).data, status=201)

class MessageDetailView(ZODBView):
    authentication_classes = [ZODBTokenAuthentication]
    
    @with_zodb
    def get(self, request, pk):
        msg = self.root['messages'].get(pk)
        if not msg: return Response(status=404)
        return Response(MessagesSerializer(msg).data)

    @with_zodb
    def delete(self, request, pk):
        if pk in self.root['messages']:
            with transaction.manager:
                del self.root['messages'][pk]
            return Response(status=204)
        return Response(status=404)

class MessageAllListView(ZODBView):
    authentication_classes = [ZODBTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @with_zodb
    def get(self, request):
        return Response([MessagesSerializer(m).data for m in self.root['messages'].values()])

class NotificationListCreateView(ZODBView):
    authentication_classes = [ZODBTokenAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    @with_zodb
    def get(self, request):
        if not self.current_user: return Response([])
        notifs = [n for n in self.root['notifications'].values() 
                  if n.user.id == self.current_user.id and not n.is_read]
        return Response([NotificationsSerializer(n).data for n in notifs])

    @with_zodb
    def post(self, request):
        text = request.data.get('text', '')
        message_id = request.data.get('message_id')
        
        if not text:
            return Response({"text": "This field is required."}, status=400)
        if not message_id:
            return Response({"message_id": "This field is required."}, status=400)
        
        msg = self.root['messages'].get(message_id)
        if not msg:
            return Response({"message_id": ["Message not found"]}, status=400)
        
        with transaction.manager:
            notif = Notifications(user=msg.user, text=text, message_id=message_id)
            self.root['notifications'][notif.id] = notif
        
        return Response(NotificationsSerializer(notif).data, status=201)

class NotificationDetailView(ZODBView):
    authentication_classes = [ZODBTokenAuthentication]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    @with_zodb
    def get(self, request, pk):
        notif = self.root['notifications'].get(pk)
        if not notif: return Response(status=404)
        if self.current_user and notif.user.id != self.current_user.id:
            return Response(status=404)
        return Response(NotificationsSerializer(notif).data)
    
    @with_zodb
    def patch(self, request, pk):
        notif = self.root['notifications'].get(pk)
        if not notif: return Response(status=404)
        if self.current_user and notif.user.id != self.current_user.id:
            return Response(status=404)
        with transaction.manager:
            notif.is_read = True
        return Response({"success": True, "message": "Marked as read"})

