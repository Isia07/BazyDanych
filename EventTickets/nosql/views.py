from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

from bson import ObjectId
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http
from rest_framework import permissions

from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from .mongo_client import (
    events_collection,
    orders_collection,
    tickets_collection,
    notifications_collection,
    messages_collection,
    discounts_collection,
    event_types_collection,
    ticket_types_collection,
    statuses_collection,
)
from .serializers import (
    StatusObjSerializer, EventTypeObjSerializer, TicketTypeObjSerializer, DiscountObjSerializer,
    EventSerializer, TicketSerializer,
    OrderSerializer, OrderCreateSerializer,
    MessageSerializer, NotificationSerializer, NotificationCreateSerializer,
)

# ---------------- helpers (nie potrzebujesz utils.py) ----------------

def oid(x: str) -> ObjectId:
    return ObjectId(str(x))

def normalize_bson(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return {k: normalize_bson(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_bson(v) for v in value]
    return value

def doc_to_api(doc: dict) -> dict:
    if not doc:
        return None
    d = dict(doc)
    d["id"] = str(d.pop("_id"))
    return normalize_bson(d)


def now():
    return timezone.now()

def serialize_event(event_doc):
    e = doc_to_api(event_doc)
    st = statuses_collection.find_one({"_id": event_doc["status_id"]})
    et = event_types_collection.find_one({"_id": event_doc["event_type_id"]})
    e["status"] = doc_to_api(st) if st else None
    e["event_type"] = doc_to_api(et) if et else None
    return e

def serialize_ticket(ticket_doc):
    t = doc_to_api(ticket_doc)
    ev = events_collection.find_one({"_id": ticket_doc["event_id"]})
    tt = ticket_types_collection.find_one({"_id": ticket_doc["ticket_type_id"]})

    t["event_detail"] = serialize_event(ev) if ev else None
    t["ticket_type"] = doc_to_api(tt) if tt else None
    t["order_id"] = str(ticket_doc["order_id"]) if ticket_doc.get("order_id") else None
    return t

def order_to_api(order_doc):
    o = doc_to_api(order_doc)
    o["user_id"] = int(order_doc["user_id"])

    disc = None
    if order_doc.get("discount_id"):
        disc = discounts_collection.find_one({"_id": order_doc["discount_id"]})
    o["discount"] = doc_to_api(disc) if disc else None

    tdocs = list(tickets_collection.find({"order_id": order_doc["_id"]}))
    o["tickets"] = [serialize_ticket(t) for t in tdocs]
    return o

# ---------------- auth (1:1 z obj-rel) ----------------

class NosqlRegisterView(BaseRegisterView):
    database = 'relational'

class NosqlLoginView(BaseLoginView):
    database = 'relational'

# ---------------- statuses ----------------

class NosqlStatusListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        docs = [doc_to_api(d) for d in statuses_collection.find({})]
        return Response(docs)

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        _id = statuses_collection.insert_one({"name": name}).inserted_id
        return Response(doc_to_api(statuses_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlStatusDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, id):
        d = statuses_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

    def put(self, request, id):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        ok = statuses_collection.update_one({"_id": oid(id)}, {"$set": {"name": name}}).matched_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(statuses_collection.find_one({"_id": oid(id)})))

    def delete(self, request, id):
        ok = statuses_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- event-types ----------------

class NosqlEventTypeListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        docs = [doc_to_api(d) for d in event_types_collection.find({})]
        return Response(docs)

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        _id = event_types_collection.insert_one({"name": name}).inserted_id
        return Response(doc_to_api(event_types_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlEventTypeDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, id):
        d = event_types_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

    def put(self, request, id):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        ok = event_types_collection.update_one({"_id": oid(id)}, {"$set": {"name": name}}).matched_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(event_types_collection.find_one({"_id": oid(id)})))

    def delete(self, request, id):
        ok = event_types_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- ticket-types ----------------

class NosqlTicketTypeListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        docs = [doc_to_api(d) for d in ticket_types_collection.find({})]
        return Response(docs)

    def post(self, request):
        ser = TicketTypeObjSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        _id = ticket_types_collection.insert_one({
            "name": v["name"],
            "discount": float(v["discount"]),
        }).inserted_id
        return Response(doc_to_api(ticket_types_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlTicketTypeDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, id):
        d = ticket_types_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

    def put(self, request, id):
        ser = TicketTypeObjSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        ok = ticket_types_collection.update_one(
            {"_id": oid(id)},
            {"$set": {"name": v["name"], "discount": float(v["discount"])}}
        ).matched_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(ticket_types_collection.find_one({"_id": oid(id)})))

    def delete(self, request, id):
        ok = ticket_types_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- discounts ----------------

class NosqlDiscountListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        docs = [doc_to_api(d) for d in discounts_collection.find({})]
        return Response(docs)

    def post(self, request):
        ser = DiscountObjSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        _id = discounts_collection.insert_one({
            "name": v["name"],
            "discount_percentage": float(v["discount_percentage"]),
            "code": v["code"],
            "valid_from": v["valid_from"],
            "valid_to": v["valid_to"],
        }).inserted_id
        return Response(doc_to_api(discounts_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlDiscountDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, id):
        d = discounts_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

    def put(self, request, id):
        ser = DiscountObjSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        ok = discounts_collection.update_one(
            {"_id": oid(id)},
            {"$set": {
                "name": v["name"],
                "discount_percentage": float(v["discount_percentage"]),
                "code": v["code"],
                "valid_from": v["valid_from"],
                "valid_to": v["valid_to"],
            }}
        ).matched_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(discounts_collection.find_one({"_id": oid(id)})))

    def delete(self, request, id):
        ok = discounts_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- events ----------------

class NosqlEventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        docs = list(events_collection.find({}))
        return Response([serialize_event(d) for d in docs])

    def post(self, request):
        ser = EventSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        payload = {
            "name": v["name"],
            "description": v["description"],
            "localization": v["localization"],
            "date_start": v["date_start"],
            "date_end": v["date_end"],
            "created_at": now(),
            "updated_at": now(),
            "base_price": float(v["base_price"]),
            "quantity": int(v["quantity"]),
            "event_type_id": oid(v["event_type_id"]),
            "status_id": oid(v["status_id"]),
        }
        _id = events_collection.insert_one(payload).inserted_id
        return Response(serialize_event(events_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlEventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        d = events_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(serialize_event(d))

    def put(self, request, id):
        ser = EventSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        ok = events_collection.update_one(
            {"_id": oid(id)},
            {"$set": {
                "name": v["name"],
                "description": v["description"],
                "localization": v["localization"],
                "date_start": v["date_start"],
                "date_end": v["date_end"],
                "updated_at": now(),
                "base_price": float(v["base_price"]),
                "quantity": int(v["quantity"]),
                "event_type_id": oid(v["event_type_id"]),
                "status_id": oid(v["status_id"]),
            }}
        ).matched_count

        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(serialize_event(events_collection.find_one({"_id": oid(id)})))

    def delete(self, request, id):
        ok = events_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- tickets ----------------

class NosqlTicketListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        docs = list(tickets_collection.find({}))
        return Response([serialize_ticket(d) for d in docs])

    def post(self, request):
        ser = TicketSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        ev = events_collection.find_one({"_id": oid(v["event"])})
        if not ev:
            return Response({"detail": "Event not found"}, status=http.HTTP_400_BAD_REQUEST)

        if int(ev["quantity"]) < int(v["quantity"]):
            return Response({"detail": f"{ev['quantity']} tickets left"}, status=http.HTTP_400_BAD_REQUEST)

        tt = ticket_types_collection.find_one({"_id": oid(v["ticket_type_id"])})
        if not tt:
            return Response({"detail": "Ticket type not found"}, status=http.HTTP_400_BAD_REQUEST)

        _id = tickets_collection.insert_one({
            "event_id": oid(v["event"]),
            "ticket_type_id": oid(v["ticket_type_id"]),
            "quantity": int(v["quantity"]),
            "order_id": None,
            "created_at": now(),
            "updated_at": now(),
        }).inserted_id

        return Response(serialize_ticket(tickets_collection.find_one({"_id": _id})), status=http.HTTP_201_CREATED)

class NosqlTicketDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        d = tickets_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(serialize_ticket(d))

    def delete(self, request, id):
        ok = tickets_collection.delete_one({"_id": oid(id)}).deleted_count
        if not ok:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)

# ---------------- orders (1:1 logika z OrderCreateSerializer) ----------------

class NosqlOrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(orders_collection.find({"user_id": request.user.id}))
        return Response([order_to_api(d) for d in docs])

    def post(self, request):
        ser = OrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        tickets_data = data["tickets"]
        discount_id = data.get("discount", None)

        discount_doc = None
        if discount_id is not None:
            discount_doc = discounts_collection.find_one({"_id": oid(discount_id)})
            if not discount_doc:
                return Response({"discount": ["Invalid discount code (not found)"]}, status=http.HTTP_400_BAD_REQUEST)
            now_dt = timezone.now()
            if discount_doc["valid_from"] > now_dt or discount_doc["valid_to"] < now_dt:
                return Response({"discount": ["Invalid discount code (check validity dates)"]}, status=http.HTTP_400_BAD_REQUEST)

        quantity_per_event = defaultdict(int)
        total = Decimal("0.00")
        quantity_to_subtract = defaultdict(int)

        for t in tickets_data:
            ev_oid = oid(t["event"])
            tt_oid = oid(t["ticket_type"])
            qty = int(t["quantity"])

            ev = events_collection.find_one({"_id": ev_oid})
            if not ev:
                return Response({"detail": "Event not found"}, status=http.HTTP_400_BAD_REQUEST)

            if qty > int(ev["quantity"]):
                return Response(
                    {"detail": f"For event '{ev['name']}' only {ev['quantity']} tickets are available, "
                               f"but you are trying to buy {qty} in one position"},
                    status=http.HTTP_400_BAD_REQUEST
                )

            quantity_per_event[str(ev_oid)] += qty

            tt = ticket_types_collection.find_one({"_id": tt_oid})
            if not tt:
                return Response({"detail": "Ticket type not found"}, status=http.HTTP_400_BAD_REQUEST)

            base_price = Decimal(str(ev["base_price"]))
            type_discount = Decimal(str(tt.get("discount", 0)))
            price_per_unit = base_price * (Decimal("1") - type_discount)
            total += price_per_unit * Decimal(qty)

            quantity_to_subtract[ev_oid] += qty

        for ev_id_str, total_qty in quantity_per_event.items():
            ev = events_collection.find_one({"_id": oid(ev_id_str)})
            if total_qty > int(ev["quantity"]):
                return Response(
                    {"detail": f"For event '{ev['name']}' only {ev['quantity']} tickets are available, "
                               f"but you are trying to buy {total_qty} in the order"},
                    status=http.HTTP_400_BAD_REQUEST
                )

        if discount_doc:
            code_factor = Decimal("1") - Decimal(str(discount_doc["discount_percentage"]))
            total = total * code_factor

        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # odejmij quantity (najprostsza ochrona przed oversell)
        for ev_oid, qty in quantity_to_subtract.items():
            ok = events_collection.update_one(
                {"_id": ev_oid, "quantity": {"$gte": qty}},
                {"$inc": {"quantity": -qty}, "$set": {"updated_at": now()}}
            ).matched_count
            if not ok:
                return Response({"detail": "Not enough tickets available (race condition)"}, status=http.HTTP_409_CONFLICT)

        order_id = orders_collection.insert_one({
            "user_id": request.user.id,
            "purchase_date": now(),
            "total_price": float(total),
            "discount_id": discount_doc["_id"] if discount_doc else None,
        }).inserted_id

        for t in tickets_data:
            tickets_collection.insert_one({
                "event_id": oid(t["event"]),
                "ticket_type_id": oid(t["ticket_type"]),
                "quantity": int(t["quantity"]),
                "order_id": order_id,
                "created_at": now(),
                "updated_at": now(),
            })

        return Response(order_to_api(orders_collection.find_one({"_id": order_id})),
                        status=http.HTTP_201_CREATED)

class NosqlOrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        d = orders_collection.find_one({"_id": oid(id), "user_id": request.user.id})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(order_to_api(d))

# ---------------- notifications ----------------

class NosqlNotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(notifications_collection.find(
            {"user_id": request.user.id, "is_read": False}
        ).sort("created_at", -1))
        return Response([doc_to_api(d) for d in docs])

    def post(self, request):
        ser = NotificationCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        msg = messages_collection.find_one({"_id": oid(v["message_id"])})
        if not msg:
            return Response({"message_id": ["Message not found"]}, status=http.HTTP_400_BAD_REQUEST)

        _id = notifications_collection.insert_one({
            "user_id": msg["user_id"],
            "text": v["text"],
            "is_read": False,
            "created_at": now(),
            "message_id": msg["_id"],
        }).inserted_id

        return Response(doc_to_api(notifications_collection.find_one({"_id": _id})),
                        status=http.HTTP_201_CREATED)

class NosqlNotificationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        d = notifications_collection.find_one({"_id": oid(id), "user_id": request.user.id})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

    def patch(self, request, id):
        d = notifications_collection.find_one({"_id": oid(id), "user_id": request.user.id})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)

        notifications_collection.update_one({"_id": oid(id)}, {"$set": {"is_read": True}})
        return Response({"success": True, "message": "Marked as read"})

# ---------------- messages ----------------

class NosqlMessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(messages_collection.find({"user_id": request.user.id}))
        return Response([doc_to_api(d) for d in docs])

    def post(self, request):
        ser = MessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        _id = messages_collection.insert_one({
            "user_id": request.user.id,
            "text": v["text"],
            "created_at": now(),
        }).inserted_id
        return Response(doc_to_api(messages_collection.find_one({"_id": _id})),
                        status=http.HTTP_201_CREATED)

class NosqlMessageDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        # obj-rel: get_queryset = Message.objects (czyli dowolny message dla zalogowanego)
        d = messages_collection.find_one({"_id": oid(id)})
        if not d:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(d))

class NosqlMessageAllListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(messages_collection.find({}).sort("created_at", -1))
        return Response([doc_to_api(d) for d in docs])