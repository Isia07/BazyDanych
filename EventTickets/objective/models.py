from django.db import models
from django.contrib.auth import get_user_model
from dataclasses import dataclass, asdict

User = get_user_model()

@dataclass
class TypeObj:
    name: str

@dataclass
class StatusObj(TypeObj):
    pass

@dataclass
class EventTypeObj(TypeObj):
    pass

@dataclass
class TicketTypeObj(TypeObj):
    pass

@dataclass
class SeatTypeObj(TypeObj):
    pass

class DiscountObj(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        db_table = "discount_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.code

class Event(models.Model):
    event_type = models.JSONField(default=dict)
    status = models.JSONField(default=dict)
    localization = models.TextField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event_obj"
        app_label = "objective"

    def set_status(self, status: StatusObj):
        self.status = asdict(status)

    def set_event_type(self, event_type: EventTypeObj):
        self.event_type = asdict(event_type)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    discount = models.ForeignKey(
        DiscountObj, on_delete=models.SET_NULL, null=True, blank=True
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ticket_obj"
        app_label = "objective"

@dataclass
class OrderTicket:
    ticket_id: int
    quantity: int
    price_per_unit: float
    subtotal: float
    ticket_types: dict
    seat_type: dict

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_orders")
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    tickets = models.JSONField(default=list)

    class Meta:
        db_table = "order_obj"
        app_label = "objective"

    def add_ticket(self, ticket: OrderTicket):
        if self.tickets is None:
            self.tickets = []
        self.tickets.append(asdict(ticket))

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_notifications")
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_obj"
        app_label = "objective"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_Messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "message_obj"
        app_label = "objective"
