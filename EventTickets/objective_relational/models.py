from django.db import models


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


class EventTypesObj(TypeObj):
    class Meta:
        db_table = "event_types_obj"
        app_label = "objective_relational"


class TicketTypesObj(TypeObj):
    class Meta:
        db_table = "ticket_types_obj"
        app_label = "objective_relational"


class SeatTypesObj(TypeObj):
    class Meta:
        db_table = "seat_types_obj"
        app_label = "objective_relational"


class UserRolesObj(TypeObj):
    class Meta:
        db_table = "user_roles_obj"
        app_label = "objective_relational"


class DiscountsObj(TypeObj):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    valid_to = models.DateTimeField()

    class Meta:
        db_table = "discounts_obj"
        app_label = "objective_relational"


class Users(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.ForeignKey(UserRolesObj, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        app_label = "objective_relational"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Events(models.Model):
    event_type = models.ForeignKey(EventTypesObj, on_delete=models.PROTECT)
    status = models.ForeignKey(StatusObj, on_delete=models.PROTECT)
    localization = models.TextField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "events"
        app_label = "objective_relational"

    def __str__(self):
        return self.name


class Tickets(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="tickets")
    discount = models.ForeignKey(
        DiscountsObj, on_delete=models.SET_NULL, null=True, blank=True
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets"
        app_label = "objective_relational"


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "orders"
        app_label = "objective_relational"


class OrderTickets(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    ticket_types = models.ForeignKey(TicketTypesObj, on_delete=models.PROTECT)
    seat_type = models.ForeignKey(SeatTypesObj, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "order_tickets"
        app_label = "objective_relational"


class Notifications(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        app_label = "objective_relational"


class Messages(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        app_label = "objective_relational"
