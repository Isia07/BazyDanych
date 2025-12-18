from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from bson import ObjectId

@dataclass
class UserDoc:
    id: Optional[ObjectId] = None
    email: str = ""
    password_hash: str = ""
    name: str = ""
    surname: str = ""
    role: str = ""        
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class DiscountDoc:
    code: str
    discount_percentage: float
    valid_from: datetime
    valid_to: datetime


@dataclass
class EventTicketDoc:
    ticket_type: str            
    seat_type: str               
    base_price: float
    quantity_available: int
    is_active: bool = True
    discount: Optional[DiscountDoc] = None


@dataclass
class EventDoc:
    id: Optional[ObjectId] = None
    name: str = ""
    description: str = ""
    localization: str = ""
    event_type: str = ""        
    status: str = ""             
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    tickets: List[EventTicketDoc] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OrderItemDoc:
    event_id: ObjectId
    event_name: str
    ticket_type: str
    seat_type: str
    quantity: int
    price_per_unit: float
    subtotal: float


@dataclass
class OrderDoc:
    id: Optional[ObjectId] = None
    user_id: ObjectId = None
    purchase_date: Optional[datetime] = None
    total_price: float = 0.0
    tickets: List[OrderItemDoc] = field(default_factory=list)


@dataclass
class NotificationDoc:
    id: Optional[ObjectId] = None
    user_id: ObjectId = None
    text: str = ""
    is_read: bool = False
    created_at: Optional[datetime] = None


@dataclass
class MessageDoc:
    id: Optional[ObjectId] = None
    user_id: ObjectId = None
    text: str = ""
    created_at: Optional[datetime] = None
