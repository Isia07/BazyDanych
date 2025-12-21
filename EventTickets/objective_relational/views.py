from rest_framework import permissions, generics
from rest_framework.response import Response
from .models import (
    Event, Ticket, Order, Notification, Message,
    StatusObj, EventTypeObj, TicketTypeObj, DiscountObj
)
from .serializers import (
    EventSerializer, TicketSerializer, OrderSerializer,
    NotificationSerializer, MessageSerializer,
    StatusObjSerializer, EventTypeObjSerializer, TicketTypeObjSerializer, DiscountObjSerializer, OrderCreateSerializer,
    NotificationCreateSerializer
)
from EventTickets.shared.views import BaseRegisterView, BaseLoginView


class RegisterView(BaseRegisterView):
    database = 'objective_relational'


class LoginView(BaseLoginView):
    database = 'objective_relational'


class StatusObjListCreateView(generics.ListCreateAPIView):
    serializer_class = StatusObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return StatusObj.objects.using("objective_relational").all()

class StatusObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StatusObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return StatusObj.objects.using("objective_relational").all()



class EventTypeObjListCreateView(generics.ListCreateAPIView):
    serializer_class = EventTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return EventTypeObj.objects.using("objective_relational").all()


class EventTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return EventTypeObj.objects.using("objective_relational").all()

class TicketTypeObjListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return TicketTypeObj.objects.using("objective_relational").all()

class TicketTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return TicketTypeObj.objects.using("objective_relational").all()


class DiscountObjListCreateView(generics.ListCreateAPIView):
    serializer_class = DiscountObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return DiscountObj.objects.using("objective_relational").all()


class DiscountObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountObjSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return DiscountObj.objects.using("objective_relational").all()


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Event.objects.using("objective_relational").select_related('event_type', 'status').all()

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Event.objects.using("objective_relational").select_related('event_type', 'status').all()


class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Ticket.objects.using("objective_relational").select_related('event', 'ticket_type', 'order').all()

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Ticket.objects.using("objective_relational").select_related('event', 'discount', 'ticket_type', 'order').all()

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.using("objective_relational").filter(user=self.request.user).prefetch_related(
            'tickets__event',
            'tickets__ticket_type',
            'tickets__discount'
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


    def get_queryset(self):
        return Order.objects.using("objective_relational").filter(user=self.request.user).prefetch_related(
            'tickets__event',
            'tickets__ticket_type',
            'tickets__discount'
        )


class NotificationListCreateView(generics.ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Notification.objects.using("objective_relational").filter(user=self.request.user, is_read=False).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Notification.objects.using("objective_relational").filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save(update_fields=['is_read'])
        return Response({"success": True, "message": "Marked as read"})


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.using("objective_relational").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


    def get_queryset(self):
        return Message.objects.using("objective_relational")

class MessageAllListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.using("objective_relational").all()
