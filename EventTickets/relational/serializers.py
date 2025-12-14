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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.using("relational").all())

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        return Message.objects.using("relational").create(**validated_data)



class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.using("relational").all())

    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, validated_data):
        return Notification.objects.using("relational").create(**validated_data)



class EventSerializer(serializers.ModelSerializer):
    event_type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.using("relational").all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.using("relational").all())

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        return Event.objects.using("relational").create(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.using("relational").all())
    ticket_type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.using("relational").all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.using("relational").all())

    class Meta:
        model = Ticket
        fields = '__all__'

