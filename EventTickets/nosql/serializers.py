from rest_framework import serializers

class StatusObjSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

class EventTypeObjSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

class TicketTypeObjSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    discount = serializers.DecimalField(max_digits=8, decimal_places=4)

class DiscountObjSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    discount_percentage = serializers.DecimalField(max_digits=8, decimal_places=2)
    code = serializers.CharField(max_length=80)
    valid_from = serializers.DateTimeField()
    valid_to = serializers.DateTimeField()

class EventSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    localization = serializers.CharField()
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    base_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    quantity = serializers.IntegerField(min_value=0)

    event_type = EventTypeObjSerializer(read_only=True)
    status = StatusObjSerializer(read_only=True)

    event_type_id = serializers.CharField(write_only=True)
    status_id = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            d = dict(data)

            if "event_type_id" not in d and "event_type" in d:
                d["event_type_id"] = d.get("event_type")

            if "status_id" not in d and "status" in d:
                d["status_id"] = d.get("status")

            return super().to_internal_value(d)

        return super().to_internal_value(data)

class TicketSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    event = serializers.CharField(write_only=True, required=False)
    event_id = serializers.CharField(write_only=True, required=False)

    event_detail = EventSerializer(read_only=True)

    ticket_type = TicketTypeObjSerializer(read_only=True)

    ticket_type_id = serializers.CharField(write_only=True, required=False)
    ticket_type_input = serializers.CharField(write_only=True, required=False)

    quantity = serializers.IntegerField(min_value=1)
    order_id = serializers.CharField(read_only=True, allow_null=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        d = dict(data)

        if "event" not in d and "event_id" in d:
            d["event"] = d["event_id"]

        if "ticket_type_id" not in d:
            if "ticket_type" in d:
                d["ticket_type_id"] = d["ticket_type"]
            elif "ticket_type_input" in d:
                d["ticket_type_id"] = d["ticket_type_input"]

        return super().to_internal_value(d)


class TicketCreateSerializer(serializers.Serializer):
    event = serializers.CharField()
    ticket_type = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    tickets = TicketCreateSerializer(many=True, write_only=True)
    discount = serializers.CharField(required=False, allow_null=True, write_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    purchase_date = serializers.DateTimeField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    tickets = TicketSerializer(many=True, read_only=True)
    discount = DiscountObjSerializer(read_only=True)
    discount_id = serializers.CharField(write_only=True, required=False, allow_null=True)

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    is_read = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

class NotificationCreateSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    is_read = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    message_id = serializers.CharField(write_only=True)
