from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeObj(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        app_label = "objective_relational"

    def __str__(self):
        return self.name


class StatusObj(TypeObj):
    class Meta:
        db_table = "status_obj"
        app_label = "objective_relational"


class EventTypeObj(TypeObj):
    class Meta:
        db_table = "event_type_obj"
        app_label = "objective_relational"


class TicketTypeObj(TypeObj):
    class Meta:
        db_table = "ticket_type_obj"
        app_label = "objective_relational"


class SeatTypeObj(TypeObj):
    class Meta:
        db_table = "seat_type_obj"
        app_label = "objective_relational"


class DiscountObj(TypeObj):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        db_table = "discount_obj"
        app_label = "objective_relational"


class Event(models.Model):
    event_type = models.ForeignKey(EventTypeObj, on_delete=models.PROTECT)
    status = models.ForeignKey(StatusObj, on_delete=models.PROTECT)
    localization = models.TextField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "event"
        app_label = "objective_relational"

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
        db_table = "ticket"
        app_label = "objective_relational"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_rel_orders")
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "order"
        app_label = "objective_relational"


class OrderTicket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_types = models.ForeignKey(TicketTypeObj, on_delete=models.PROTECT)
    seat_type = models.ForeignKey(SeatTypeObj, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "order_ticket"
        app_label = "objective_relational"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_rel_notifications")
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"
        app_label = "objective_relational"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_rel_Messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "message"
        app_label = "objective_relational"
