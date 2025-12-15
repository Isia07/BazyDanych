from rest_framework import serializers

from .models import (
    Discounts,
    Events,
    EventTypes,
    Messages,
    Notifications,
    Orders,
    Status,
    Tickets,
    TicketTypes,
    Users,
)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class EventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypes
        fields = "__all__"


class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discounts
        fields = "__all__"


class TicketTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTypes
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"
