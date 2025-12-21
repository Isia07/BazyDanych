from rest_framework.response import Response

from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework import generics, permissions
from .models import Discount, TicketType, Status, EventType, Message, Notification, Event, Ticket, Order
from .serializers import DiscountSerializer, TicketTypeSerializer, StatusSerializer, EventTypeSerializer, \
    MessageSerializer, NotificationSerializer, EventSerializer, OrderSerializer, \
    OrderCreateSerializer, NotificationCreateSerializer
from ..objective_relational.serializers import TicketSerializer


class RelRegisterView(BaseRegisterView):
    database = 'relational'


class RelLoginView(BaseLoginView):
    database = 'relational'


class RelDiscountListCreateView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelDiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelTicketTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelTicketTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelStatusListCreateView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Status.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Status.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelEventTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = EventTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return EventType.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelEventTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventTypeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return EventType.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.using("relational").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RelMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.using("relational").filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelNotificationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.using("relational").filter(user=self.request.user, is_read=False).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer


class RelNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.using("relational").filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save(update_fields=['is_read'])
        return Response({"success": True, "message": "Marked as read"})

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelEventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Event.objects.select_related('event_type', 'status').using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Event.objects.using("relational").select_related('event_type', 'status').all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelTicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Ticket.objects.using("relational").select_related('event', 'ticket_type', 'order').all()

    def perform_create(self, serializer):
        serializer.save()


class RelTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Ticket.objects.using("relational").select_related('event', 'discount', 'ticket_type', 'order').all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelOrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.using("relational").filter(user=self.request.user).prefetch_related(
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


class RelOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.using('relational').filter(user=self.request.user).prefetch_related(
            'tickets__event',
            'tickets__ticket_type',
            'tickets__discount'
        )

class RelMessageAllListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.using("relational").all()
