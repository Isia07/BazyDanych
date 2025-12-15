from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "status"
        app_label = "relational"

    def __str__(self):
        return self.name



class EventType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "eventtype"
        app_label = "relational"

    def __str__(self):
        return self.name



class TicketType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=4, default=0, validators=[
        MinValueValidator(Decimal('0.0000')),
        MaxValueValidator(Decimal('1.0000')),
    ])

    class Meta:
        db_table = "tickettype"
        app_label = "relational"

    def __str__(self):
        return self.name



class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default='')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        db_table = "discount"
        app_label = "relational"

    def __str__(self):
        return self.code



class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    localization = models.TextField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "revent"
        app_label = "relational"

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "rorder"
        app_label = "relational"


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')

    class Meta:
        db_table = "rticket"
        app_label = "relational"



class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rnotification"
        app_label = "relational"



class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rmessage"
        app_label = "relational"


