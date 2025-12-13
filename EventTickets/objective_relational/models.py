from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeObj(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        db_table = "type_obj"
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
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.0000,
        validators=[
            MinValueValidator(Decimal('0.0000')),
            MaxValueValidator(Decimal('1.0000'))
        ],
    ) # between 0 - 1

    class Meta:
        db_table = "ticket_type_obj"
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
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "event"
        app_label = "objective_relational"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketTypeObj, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(
        'Order', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ticket"
        app_label = "objective_relational"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_rel_orders")
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.ForeignKey(
        DiscountObj, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table = "order"
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obj_rel_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "message"
        app_label = "objective_relational"
