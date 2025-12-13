from collections import defaultdict

from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from rest_framework import serializers
from .models import (
    Event, Ticket, Order, Notification, Message,
    StatusObj, EventTypeObj, TicketTypeObj, DiscountObj
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
        fields = ('id', 'name', 'discount')


class DiscountObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountObj
        fields = ('id', 'name', 'discount_percentage', 'code', 'valid_from', 'valid_to')


class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeObjSerializer(read_only=True)
    event_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EventTypeObj.objects.all(), source='event_type', write_only=True
    )
    status = StatusObjSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusObj.objects.all(), source='status', write_only=True
    )

    class Meta:
        model = Event
        fields = (
            'id', 'name', 'description', 'localization',
            'date_start', 'date_end', 'created_at', 'updated_at',
            'base_price', 'quantity',
            'event_type', 'event_type_id', 'status', 'status_id'
        )
        read_only_fields = ('created_at', 'updated_at')


class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), write_only=True
    )
    event_detail = EventSerializer(source='event', read_only=True)
    ticket_type = TicketTypeObjSerializer(read_only=True)
    ticket_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketTypeObj.objects.all(), source='ticket_type', write_only=True
    )
    order_id = serializers.IntegerField(source='order.id', read_only=True, allow_null=True)

    class Meta:
        model = Ticket
        fields = (
            'id', 'event', 'event_detail',
            'ticket_type', 'ticket_type_id',
            'quantity', 'order_id',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'order_id')


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


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('event', 'ticket_type', 'quantity')

    def validate(self, attrs):
        event = attrs['event']
        quantity = attrs['quantity']

        if event.quantity < quantity:
            raise serializers.ValidationError(
                f"{event.quantity} tickets left"
            )
        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, write_only=True)
    discount = serializers.PrimaryKeyRelatedField(
        queryset=DiscountObj.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'purchase_date', 'total_price', 'tickets', 'discount')
        read_only_fields = ('purchase_date', 'total_price')

    def validate_discount(self, value):
        if value is not None:
            now = timezone.now()
            if value.valid_from > now or value.valid_to < now:
                raise serializers.ValidationError("Invalid discount code (check validity dates)")
        return value

    def validate_tickets(self, tickets_data):
        quantity_per_event = defaultdict(int)

        for ticket_data in tickets_data:
            event = ticket_data['event']
            qty = ticket_data['quantity']
            quantity_per_event[event.id] += qty

            if qty > event.quantity:
                raise serializers.ValidationError(
                    f"For event '{event.name}' only {event.quantity} tickets are available, but you are trying to buy {qty} in one position"
                )

        for event_id, total_qty in quantity_per_event.items():
            event = next(t['event'] for t in tickets_data if t['event'].id == event_id)
            if total_qty > event.quantity:
                raise serializers.ValidationError(
                    f"For event '{event.name}' only {event.quantity} tickets are available, "
                    f"but you are trying to buy {total_qty} in the order"
                )

        return tickets_data

    def validate(self, data):
        data['tickets'] = self.validate_tickets(data['tickets'])
        return data

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        discount_obj = validated_data.pop('discount', None)

        request = self.context['request']
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal('0.00'),
            discount=discount_obj
        )

        total = Decimal('0.00')

        quantity_to_subtract = defaultdict(int)

        for ticket_data in tickets_data:
            event = ticket_data['event']
            base_price = event.base_price
            quantity = Decimal(ticket_data['quantity'])
            ticket_type = ticket_data['ticket_type']
            type_discount = ticket_type.discount

            price_per_unit = base_price * (Decimal('1') - type_discount)
            subtotal = price_per_unit * quantity
            total += subtotal

            Ticket.objects.create(order=order, **ticket_data)

            quantity_to_subtract[event] += ticket_data['quantity']

        if order.discount:
            code_factor = Decimal('1') - order.discount.discount_percentage
            total = total * code_factor

        total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        order.total_price = total
        order.save()

        for event, qty in quantity_to_subtract.items():
            event.quantity -= qty
            event.save(update_fields=['quantity'])

        return order

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    discount = DiscountObjSerializer(read_only=True)
    discount_id = serializers.PrimaryKeyRelatedField(
        queryset=DiscountObj.objects.all(),
        source='discount',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = (
            'id', 'user_id', 'purchase_date', 'total_price',
            'tickets', 'discount', 'discount_id'
        )
        read_only_fields = ('purchase_date', 'total_price', 'user_id')
