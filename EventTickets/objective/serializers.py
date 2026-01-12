from rest_framework import serializers

class StatusSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)

class EventTypesSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)

class DiscountsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    code = serializers.CharField(max_length=50)
    valid_from = serializers.DateTimeField()
    valid_to = serializers.DateTimeField()
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)

class TicketTypesSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class EventsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    localization = serializers.CharField()
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    event_type = EventTypesSerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    event_type_id = serializers.CharField(write_only=True, required=False)
    status_id = serializers.CharField(write_only=True, required=False)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            d = dict(data)
            if "event_type_id" not in d and "event_type" in d:
                d["event_type_id"] = d.get("event_type")
            if "status_id" not in d and "status" in d:
                d["status_id"] = d.get("status")
            return super().to_internal_value(d)
        return super().to_internal_value(data)

class OrdersSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    purchase_date = serializers.DateTimeField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    user_id = serializers.CharField(read_only=True) # or nested user?
    discount = DiscountsSerializer(read_only=True, allow_null=True)
    
    tickets_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    tickets = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    discount_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    tickets_list = serializers.SerializerMethodField()
    
    def get_tickets_list(self, obj):
        if hasattr(obj, 'tickets'):
            return [TicketsSerializer(t).data for t in obj.tickets]
        return []
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tickets'] = ret.pop('tickets_list', [])
        return ret

class TicketsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    event = EventsSerializer(read_only=True)
    order_id = serializers.CharField(read_only=True)
    ticket_type = TicketTypesSerializer(read_only=True)
    
    event_id = serializers.CharField(write_only=True)
    ticket_type_id = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        d = dict(data)
        if "event" in d and "event_id" not in d:
            d["event_id"] = d["event"]
        if "ticket_type" in d and "ticket_type_id" not in d:
            d["ticket_type_id"] = d["ticket_type"]
        return super().to_internal_value(d)

class MessagesSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.CharField(read_only=True)

class NotificationsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    is_read = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.CharField(read_only=True)
