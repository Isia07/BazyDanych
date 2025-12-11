from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
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


class StatusObjListCreateView(generics.ListCreateAPIView):
    queryset = StatusObj.objects.all()
    serializer_class = StatusObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class StatusObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StatusObj.objects.all()
    serializer_class = StatusObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EventTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = EventTypeObj.objects.all()
    serializer_class = EventTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class EventTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventTypeObj.objects.all()
    serializer_class = EventTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class TicketTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = TicketTypeObj.objects.all()
    serializer_class = TicketTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class TicketTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketTypeObj.objects.all()
    serializer_class = TicketTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class SeatTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = SeatTypeObj.objects.all()
    serializer_class = SeatTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class SeatTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeatTypeObj.objects.all()
    serializer_class = SeatTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class DiscountObjListCreateView(generics.ListCreateAPIView):
    queryset = DiscountObj.objects.all()
    serializer_class = DiscountObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class DiscountObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscountObj.objects.all()
    serializer_class = DiscountObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.select_related('event_type', 'status').all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related('event_type', 'status').all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.select_related('event', 'discount').all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.select_related('event', 'discount').all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'orderticket_set__ticket',
            'orderticket_set__ticket_types',
            'orderticket_set__seat_type'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'orderticket_set__ticket',
            'orderticket_set__ticket_types',
            'orderticket_set__seat_type'
        )


class OrderTicketListCreateView(generics.ListCreateAPIView):
    queryset = OrderTicket.objects.select_related(
        'ticket__event', 'ticket_types', 'seat_type', 'order'
    ).all()
    serializer_class = OrderTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        ticket_id = self.request.query_params.get('ticket_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        if ticket_id:
            queryset = queryset.filter(ticket_id=ticket_id)
        return queryset


class OrderTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderTicket.objects.select_related(
        'ticket__event', 'ticket_types', 'seat_type', 'order'
    ).all()
    serializer_class = OrderTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save(update_fields=['is_read'])
        return Response({"success": True, "message": "Marked as read"})


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)
