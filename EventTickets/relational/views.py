from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework import status, generics
from .models import Discount, TicketType, Status, EventType, Message, Notification, Event
from .serializers import DiscountSerializer, TicketTypeSerializer, StatusSerializer, EventTypeSerializer, \
    MessageSerializer, NotificationSerializer, EventSerializer


class RelRegisterView(BaseRegisterView):
    database = 'relational'


class RelLoginView(BaseLoginView):
    database = 'relational'


class RelDiscountListCreateView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelDiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")



class RelTicketTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketTypeSerializer

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()

class RelTicketTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeSerializer

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")



class RelStatusListCreateView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()

class RelStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelEventTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = EventTypeSerializer

    def get_queryset(self):
        return EventType.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelEventTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventTypeSerializer

    def get_queryset(self):
        return EventType.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")


class RelMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()

class RelMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")



class RelNotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()

class RelNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")

class RelEventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")