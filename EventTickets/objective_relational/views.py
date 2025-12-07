from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import (
    Event, Ticket, Order, OrderTicket, Notification, Message,
    StatusObj, EventTypeObj, TicketTypeObj, SeatTypeObj, DiscountObj
)
from .serializers import (
    EventSerializer, TicketSerializer, OrderSerializer,
    OrderTicketSerializer, NotificationSerializer, MessageSerializer,
    StatusObjSerializer, EventTypeObjSerializer, TicketTypeObjSerializer,
    SeatTypeObjSerializer, DiscountObjSerializer
)


class RegisterView(BaseRegisterView):
    database = 'objective_relational'


class LoginView(BaseLoginView):
    database = 'objective_relational'


class StatusObjListCreateView(APIView):
    """GET + POST dla StatusObj (np. "planned", "ongoing", "cancelled", "finished")"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objs = StatusObj.objects.all()
        serializer = StatusObjSerializer(objs, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = StatusObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventTypeObjListCreateView(APIView):
    """GET + POST dla EventTypeObj (np. "concert", "theater", "conference")"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objs = EventTypeObj.objects.all()
        serializer = EventTypeObjSerializer(objs, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = EventTypeObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TicketTypeObjListCreateView(APIView):
    """GET + POST dla TicketTypeObj (np. "normal", "student", "VIP")"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objs = TicketTypeObj.objects.all()
        serializer = TicketTypeObjSerializer(objs, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = TicketTypeObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SeatTypeObjListCreateView(APIView):
    """GET + POST dla SeatTypeObj (np. "standing", "seated", "VIP box")"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objs = SeatTypeObj.objects.all()
        serializer = SeatTypeObjSerializer(objs, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = SeatTypeObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DiscountObjListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        discounts = DiscountObj.objects.all()
        serializer = DiscountObjSerializer(discounts, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = DiscountObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# === Main resources ===
class EventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        events = Event.objects.select_related('event_type', 'status').all()
        serializer = EventSerializer(events, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.select_related('event_type', 'status').get(pk=pk)
        except Event.DoesNotExist:
            return None

    def get(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response({"success": True, "message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Ticket views
class TicketListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.select_related('event', 'discount').all()
        serializer = TicketSerializer(tickets, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Order views (user can only see own orders)
class UserOrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('orderticket_set__ticket_types',
                                                                          'orderticket_set__seat_type')
        serializer = OrderSerializer(orders, many=True)
        return Response({"success": True, "data": serializer.data})


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = OrderSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "data": OrderSerializer(order, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Notification & Message (user-specific)
class UserNotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response({"success": True, "data": serializer.data})

    def patch(self, request, pk):  # mark as read
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({"success": False, "error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        notif.is_read = True
        notif.save()
        return Response({"success": True, "message": "Notification marked as read"})


class UserMessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(user=request.user).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
