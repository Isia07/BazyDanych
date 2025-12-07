from rest_framework import serializers
from .models import (
    Event, Ticket, Order, OrderTicket, Notification, Message,
    StatusObj, EventTypeObj, TicketTypeObj, SeatTypeObj, DiscountObj
)
from django.contrib.auth import get_user_model

User = get_user_model()


class StatusObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusObj
        fields = ('id', 'name')


class EventTypeObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypeObj
        fields = ('id', 'name')


class TicketTypeObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTypeObj
        fields = ('id', 'name')


class SeatTypeObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatTypeObj
        fields = ('id', 'name')


class DiscountObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountObj
        fields = ('id', 'name', 'discount_percentage', 'code', 'valid_from', 'valid_to')


# === Main models ===
class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeObjSerializer(read_only=True)
    event_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EventTypeObj.objects.all(),
        source='event_type',
        write_only=True
    )
    status = StatusObjSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusObj.objects.all(),
        source='status',
        write_only=True
    )

    class Meta:
        model = Event
        fields = (
            'id', 'name', 'description', 'localization',
            'date_start', 'date_end', 'created_at', 'updated_at',
            'event_type', 'event_type_id', 'status', 'status_id'
        )


class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    discount = DiscountObjSerializer(read_only=True)
    discount_id = serializers.PrimaryKeyRelatedField(
        queryset=DiscountObj.objects.all(),
        source='discount',
        allow_null=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Ticket
        fields = (
            'id', 'event', 'base_price', 'quantity', 'is_active',
            'discount', 'discount_id', 'created_at', 'updated_at'
        )


class OrderTicketSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    ticket_types = TicketTypeObjSerializer(read_only=True)
    ticket_types_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketTypeObj.objects.all(),
        source='ticket_types',
        write_only=True
    )
    seat_type = SeatTypeObjSerializer(read_only=True)
    seat_type_id = serializers.PrimaryKeyRelatedField(
        queryset=SeatTypeObj.objects.all(),
        source='seat_type',
        write_only=True
    )

    class Meta:
        model = OrderTicket
        fields = (
            'id', 'ticket', 'ticket_types', 'ticket_types_id',
            'seat_type', 'seat_type_id', 'quantity',
            'price_per_unit', 'subtotal'
        )


class OrderSerializer(serializers.ModelSerializer):
    order_tickets = OrderTicketSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'purchase_date', 'total_price', 'order_tickets')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'text', 'is_read', 'created_at')
        read_only_fields = ('created_at',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at')
        read_only_fields = ('created_at',)