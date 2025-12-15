from collections import defaultdict
from decimal import Decimal

from _decimal import ROUND_HALF_UP
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import Discount, TicketType, Status, EventType, User, Message, Notification, Event, Ticket, Order


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'code': {'validators': []},
        }

    def validate_code(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.code == value:
                return value

        if Discount.objects.using('relational').filter(code=value).exists():
            raise serializers.ValidationError("Code already exists.")
        return value

    def create(self, validated_data):
        return Discount.objects.using("relational").create(**validated_data)


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
    }

    def validate_name(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.name == value:
                return value

        if TicketType.objects.using('relational').filter(name=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def create(self, validated_data):
        return TicketType.objects.using("relational").create(**validated_data)

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }

    def validate_name(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.name == value:
                return value

        if Status.objects.using('relational').filter(name=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def create(self, validated_data):
        return Status.objects.using('relational').create(**validated_data)


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': [] }
        }

    def validate_name(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.name == value:
                return value

        if EventType.objects.using('relational').filter(name=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def create(self, validated_data):
        return EventType.objects.using("relational").create(**validated_data)



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']

    def create(self, validated_data):
        return Message.objects.using("relational").create(**validated_data)



class NotificationCreateSerializer(serializers.ModelSerializer):
    message_id = serializers.PrimaryKeyRelatedField(
        queryset=Message.objects.using('relational').all(),
        write_only=True
    )

    class Meta:
        model = Notification
        fields = ['id', 'text', 'is_read', 'created_at', 'message_id']
        read_only_fields = ['id', 'is_read', 'created_at']

    def create(self, validated_data):
        message = validated_data.pop('message_id')
        validated_data['user'] = message.user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'text', 'is_read', 'created_at')
        read_only_fields = ('created_at',)


class EventSerializer(serializers.ModelSerializer):
    event_type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.using("relational").all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.using("relational").all())

    class Meta:
        model = Event
        fields = [ 'id', 'name', 'description', 'localization',
            'date_start', 'date_end', 'created_at', 'updated_at',
            'base_price', 'quantity',
            'event_type', 'status']

    def create(self, validated_data):
        return Event.objects.using("relational").create(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.using("relational").all())
    ticket_type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.using("relational").all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.using("relational").all())

    class Meta:
        model = Ticket
        fields = '__all__'

    def validate(self, attrs):
        event = attrs['event']
        quantity = attrs['quantity']

        if event.quantity < quantity:
            raise serializers.ValidationError(
                f"{event.quantity} tickets left"
            )
        return attrs



class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, write_only=True)
    discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(),required=False, allow_null=True, write_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['purchase_date', 'total_price']

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
    discount = DiscountSerializer(read_only=True)
    discount_id = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(), source='discount', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['__all__']
        read_only_fields = ['purchase_date', 'total_price', 'user_id']

