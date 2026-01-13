from persistent import Persistent
import uuid
import time
from datetime import datetime

class BasePersistent(Persistent):
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        for k, v in kwargs.items():
            setattr(self, k, v)

class Users(BasePersistent):
    def __init__(self, email, password_hash, name, surname, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.surname = surname
        self.is_active = True
        self.is_admin = False
        self.groups = []
        self.user_permissions = []

class Status(BasePersistent):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

class EventTypes(BasePersistent):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

class Discounts(BasePersistent):
    def __init__(self, code, discount_percentage, valid_from, valid_to, name="", **kwargs):
        super().__init__(**kwargs)
        self.code = code
        self.discount_percentage = discount_percentage
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.name = name

class TicketTypes(BasePersistent):
    def __init__(self, name, discount=0.0, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.discount = discount

class Events(BasePersistent):
    def __init__(self, name, description, localization, date_start, date_end, base_price, quantity, event_type, status, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.localization = localization
        self.date_start = date_start
        self.date_end = date_end
        self.base_price = base_price
        self.quantity = quantity
        self.event_type = event_type
        self.status = status

class Orders(BasePersistent):
    def __init__(self, user, total_price, discount=None, purchase_date=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.total_price = total_price
        self.discount = discount
        self.purchase_date = purchase_date or datetime.now()
        self.tickets = []

class Tickets(BasePersistent):
    def __init__(self, event, order, ticket_type, quantity, **kwargs):
        super().__init__(**kwargs)
        self.event = event
        self.order = order
        self.ticket_type = ticket_type
        self.quantity = quantity

class Messages(BasePersistent):
    def __init__(self, user, text, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.text = text

class Notifications(BasePersistent):
    def __init__(self, user, text, message_id=None, is_read=False, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.text = text
        self.message_id = message_id
        self.is_read = is_read

class Token(BasePersistent):
    def __init__(self, key, user, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.user = user
