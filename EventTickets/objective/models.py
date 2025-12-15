from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    is_admin = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fix: Add unique related_names to avoid clash with shared.User
    groups = models.ManyToManyField(
        Group,
        related_name="objective_users_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="objective_users_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    REQUIRED_FIELDS = ["name", "surname"]
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.email


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "status_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.name


class EventTypes(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "event_types_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.name


class Discounts(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        db_table = "discounts_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.code


class TicketTypes(models.Model):
    name = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "ticket_types_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.name


class Events(models.Model):
    event_type = models.ForeignKey(EventTypes, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    localization = models.TextField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "events_obj_obj"
        app_label = "objective"

    def __str__(self):
        return self.name


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    discount = models.ForeignKey(
        Discounts, on_delete=models.SET_NULL, null=True, blank=True
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "orders_obj_obj"
        app_label = "objective"

    def __str__(self):
        return str(self.id)


class Tickets(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketTypes, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets_obj_obj"
        app_label = "objective"

    def __str__(self):
        return str(self.id)


class Messages(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages_obj_obj"
        app_label = "objective"


class Notifications(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications_obj_obj"
        app_label = "objective"
