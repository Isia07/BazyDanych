import secrets
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

import bcrypt
import pytz
from bson import ObjectId
from bson.errors import InvalidId
from django.utils import timezone as dj_tz
from rest_framework import permissions
from rest_framework import status as http
from rest_framework.response import Response
from rest_framework.views import APIView

from .mongo_client import (
    events_collection,
    orders_collection,
    tickets_collection,
    notifications_collection,
    messages_collection,
    discounts_collection,
    event_types_collection,
    ticket_types_collection,
    statuses_collection,
    tokens_collection,
    users_collection,
)
from .serializers import (
    TicketTypeSerializer,
    DiscountSerializer,
    EventSerializer,
    TicketSerializer,
    OrderCreateSerializer,
    MessageSerializer,
    NotificationCreateSerializer,
)
from .token_auth import MongoTokenAuthentication


def issue_token(user_oid: ObjectId) -> str:
    key = secrets.token_hex(20)
    tokens_collection.insert_one({
        "_id": key,
        "user_id": user_oid,
        "created_at": datetime.now(),
    })
    return key


def normalize_bson(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return {k: normalize_bson(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_bson(v) for v in value]
    return value


def doc_to_api(doc: dict | None) -> dict | None:
    if not doc:
        return None
    d = dict(doc)
    d["id"] = str(d.pop("_id"))
    return normalize_bson(d)


def now():
    return dj_tz.now()


def serialize_event(event_doc):
    e = doc_to_api(event_doc)

    if event_doc.get("status_id"):
        e["status"] = str(event_doc["status_id"])
    else:
        e["status"] = None

    if event_doc.get("event_type_id"):
        e["event_type"] = str(event_doc["event_type_id"])
    else:
        e["event_type"] = None

    return e


def serialize_ticket(ticket_doc):
    t = doc_to_api(ticket_doc)
    if ticket_doc.get("event_id"):
        ev = events_collection.find_one({"_id": ticket_doc["event_id"]})
        t["event_detail"] = serialize_event(ev) if ev else None
    if ticket_doc.get("ticket_type_id"):
        tt = ticket_types_collection.find_one({"_id": ticket_doc["ticket_type_id"]})
        t["ticket_type"] = doc_to_api(tt) if tt else None
    t["order_id"] = str(ticket_doc["order_id"]) if ticket_doc.get("order_id") else None
    return t


def order_to_api(order_doc):
    o = doc_to_api(order_doc)
    o["user_id"] = str(order_doc["user_id"]) if order_doc.get("user_id") else None

    if order_doc.get("discount_id"):
        disc = discounts_collection.find_one({"_id": order_doc["discount_id"]})
        o["discount"] = doc_to_api(disc) if disc else None

    tdocs = list(tickets_collection.find({"order_id": order_doc["_id"]}))
    o["tickets"] = [serialize_ticket(t) for t in tdocs]
    return o


class NosqlRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""

        if not email or not password:
            return Response({"success": False, "error": "email and password required"}, status=400)

        if users_collection.find_one({"email": email}):
            return Response({"success": False, "error": "This email is already taken"}, status=400)

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        doc = {
            "email": email,
            "password_hash": pw_hash,
            "name": "",
            "surname": "",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        user_id = users_collection.insert_one(doc).inserted_id
        token = issue_token(user_id)

        return Response(
            {"success": True, "token": token, "user": {"id": str(user_id), "email": email}},
            status=201
        )


class NosqlLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""

        doc = users_collection.find_one({"email": email})
        if not doc or not bcrypt.checkpw(password.encode("utf-8"), doc["password_hash"].encode("utf-8")):
            return Response({"success": False, "error": "Invalid credentials"}, status=400)

        if not doc.get("is_active", True):
            return Response({"success": False, "error": "Account deactivated"}, status=400)

        token = issue_token(doc["_id"])
        return Response({"token": token, "user": {"id": str(doc["_id"]), "email": email}}, status=200)


class NosqlStatusListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response([doc_to_api(d) for d in statuses_collection.find({})])

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        inserted = statuses_collection.insert_one({"name": name})
        return Response(doc_to_api(statuses_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlStatusDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]

    def get_object(self, pk: str):
        try:
            return statuses_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))

    def put(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        statuses_collection.update_one({"_id": ObjectId(pk)}, {"$set": {"name": name}})
        return Response(doc_to_api(statuses_collection.find_one({"_id": ObjectId(pk)})))

    def delete(self, request, pk):
        result = statuses_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlEventTypeListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response([doc_to_api(d) for d in event_types_collection.find({})])

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        inserted = event_types_collection.insert_one({"name": name})
        return Response(doc_to_api(event_types_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlEventTypeDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]

    def get_object(self, pk: str):
        try:
            return event_types_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))

    def put(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        name = request.data.get("name")
        if not name:
            return Response({"name": "This field is required."}, status=http.HTTP_400_BAD_REQUEST)
        event_types_collection.update_one({"_id": ObjectId(pk)}, {"$set": {"name": name}})
        return Response(doc_to_api(event_types_collection.find_one({"_id": ObjectId(pk)})))

    def delete(self, request, pk):
        result = event_types_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlTicketTypeListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response([doc_to_api(d) for d in ticket_types_collection.find({})])

    def post(self, request):
        ser = TicketTypeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        inserted = ticket_types_collection.insert_one({
            "name": v["name"],
            "discount": float(v["discount"]),
        })
        return Response(doc_to_api(ticket_types_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlTicketTypeDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]

    def get_object(self, pk: str):
        try:
            return ticket_types_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))

    def put(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        ser = TicketTypeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        ticket_types_collection.update_one(
            {"_id": ObjectId(pk)},
            {"$set": {"name": v["name"], "discount": float(v["discount"])}}
        )
        return Response(doc_to_api(ticket_types_collection.find_one({"_id": ObjectId(pk)})))

    def delete(self, request, pk):
        result = ticket_types_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlDiscountListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response([doc_to_api(d) for d in discounts_collection.find({})])

    def post(self, request):
        ser = DiscountSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        inserted = discounts_collection.insert_one({
            "name": v["name"],
            "discount_percentage": float(v["discount_percentage"]),
            "code": v["code"],
            "valid_from": v["valid_from"],
            "valid_to": v["valid_to"],
        })
        return Response(doc_to_api(discounts_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlDiscountDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]

    def get_object(self, pk: str):
        try:
            return discounts_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))

    def put(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        ser = DiscountSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        discounts_collection.update_one(
            {"_id": ObjectId(pk)},
            {"$set": {
                "name": v["name"],
                "discount_percentage": float(v["discount_percentage"]),
                "code": v["code"],
                "valid_from": v["valid_from"],
                "valid_to": v["valid_to"],
            }}
        )
        return Response(doc_to_api(discounts_collection.find_one({"_id": ObjectId(pk)})))

    def delete(self, request, pk):
        result = discounts_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlEventListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        docs = list(events_collection.find({}))
        return Response([serialize_event(d) for d in docs])

    def post(self, request):
        ser = EventSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        payload = {
            "name": v["name"],
            "description": v["description"],
            "localization": v["localization"],
            "date_start": v["date_start"],
            "date_end": v["date_end"],
            "created_at": now(),
            "updated_at": now(),
            "base_price": float(v["base_price"]),
            "quantity": int(v["quantity"]),
            "event_type_id": ObjectId(v["event_type_id"]),
            "status_id": ObjectId(v["status_id"]),
        }

        result = events_collection.insert_one(payload)
        return Response(serialize_event(events_collection.find_one({"_id": result.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlEventDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk: str):
        try:
            return events_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(serialize_event(doc))

    def put(self, request, pk):
        if self.get_object(pk) is None:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)

        ser = EventSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        events_collection.update_one(
            {"_id": ObjectId(pk)},
            {"$set": {
                "name": v["name"],
                "description": v["description"],
                "localization": v["localization"],
                "date_start": v["date_start"],
                "date_end": v["date_end"],
                "updated_at": now(),
                "base_price": float(v["base_price"]),
                "quantity": int(v["quantity"]),
                "event_type_id": ObjectId(v["event_type_id"]),
                "status_id": ObjectId(v["status_id"]),
            }}
        )
        return Response(serialize_event(events_collection.find_one({"_id": ObjectId(pk)})))

    def delete(self, request, pk):
        result = events_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlTicketListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        docs = list(tickets_collection.find({}))
        return Response([serialize_ticket(d) for d in docs])

    def post(self, request):
        ser = TicketSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        try:
            event_id = ObjectId(v["event"])
            ticket_type_id = ObjectId(v["ticket_type_id"])
        except InvalidId:
            return Response({"detail": "Invalid event or ticket_type id"}, status=http.HTTP_400_BAD_REQUEST)

        ev = events_collection.find_one({"_id": event_id})
        if not ev:
            return Response({"detail": "Event not found"}, status=http.HTTP_400_BAD_REQUEST)

        if ev["quantity"] < v["quantity"]:
            return Response({"detail": f"Only {ev['quantity']} tickets left"}, status=http.HTTP_400_BAD_REQUEST)

        tt = ticket_types_collection.find_one({"_id": ticket_type_id})
        if not tt:
            return Response({"detail": "Ticket type not found"}, status=http.HTTP_400_BAD_REQUEST)

        inserted = tickets_collection.insert_one({
            "event_id": event_id,
            "ticket_type_id": ticket_type_id,
            "quantity": v["quantity"],
            "order_id": None,
            "created_at": now(),
            "updated_at": now(),
        })

        return Response(serialize_ticket(tickets_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlTicketDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk: str):
        try:
            return tickets_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(serialize_ticket(doc))

    def delete(self, request, pk):
        result = tickets_collection.delete_one({"_id": ObjectId(pk)})
        if result.deleted_count == 0:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(status=http.HTTP_204_NO_CONTENT)


class NosqlOrderListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(orders_collection.find({"user_id": ObjectId(request.user.id)}))
        return Response([order_to_api(d) for d in docs])

    def post(self, request):
        ser = OrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        tickets_data = data["tickets"]
        discount_id_str = data.get("discount")

        discount_doc = None
        if discount_id_str:
            try:
                discount_id = ObjectId(discount_id_str)
            except InvalidId:
                return Response(
                    {"discount": ["Invalid discount ID format"]},
                    status=http.HTTP_400_BAD_REQUEST
                )

            discount_doc = discounts_collection.find_one({"_id": discount_id})
            if not discount_doc:
                return Response(
                    {"discount": ["Discount not found"]},
                    status=http.HTTP_400_BAD_REQUEST
                )

            now_dt = dj_tz.now()

            valid_from = discount_doc.get("valid_from")
            valid_to = discount_doc.get("valid_to")

            if valid_from and dj_tz.is_naive(valid_from):
                valid_from = dj_tz.make_aware(valid_from, timezone=pytz.UTC)
            if valid_to and dj_tz.is_naive(valid_to):
                valid_to = dj_tz.make_aware(valid_to, timezone=pytz.UTC)

            if valid_from and valid_from > now_dt:
                return Response({"discount": ["Discount not yet valid"]}, status=http.HTTP_400_BAD_REQUEST)
            if valid_to and valid_to < now_dt:
                return Response({"discount": ["Discount expired"]}, status=http.HTTP_400_BAD_REQUEST)

        total = Decimal("0.00")
        quantity_to_subtract = defaultdict(int)

        for t in tickets_data:
            try:
                event_id = ObjectId(t["event"])
                ticket_type_id = ObjectId(t["ticket_type"])
            except InvalidId:
                return Response({"detail": "Invalid event or ticket_type id"}, status=http.HTTP_400_BAD_REQUEST)

            qty = int(t["quantity"])
            ev = events_collection.find_one({"_id": event_id})
            if not ev:
                return Response({"detail": "Event not found"}, status=http.HTTP_400_BAD_REQUEST)

            if qty > ev["quantity"]:
                return Response(
                    {"detail": f"Not enough tickets for event {ev['name']}"},
                    status=http.HTTP_400_BAD_REQUEST
                )

            tt = ticket_types_collection.find_one({"_id": ticket_type_id})
            if not tt:
                return Response({"detail": "Ticket type not found"}, status=http.HTTP_400_BAD_REQUEST)

            base_price = Decimal(str(ev["base_price"]))
            type_discount = Decimal(str(tt.get("discount", 0)))
            price_per_unit = base_price * (Decimal("1") - type_discount)
            total += price_per_unit * Decimal(qty)

            quantity_to_subtract[event_id] += qty

        if discount_doc:
            total *= (Decimal("1") - Decimal(str(discount_doc["discount_percentage"])))

        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        for ev_id, qty in quantity_to_subtract.items():
            result = events_collection.update_one(
                {"_id": ev_id, "quantity": {"$gte": qty}},
                {"$inc": {"quantity": -qty}, "$set": {"updated_at": now()}}
            )
            if result.matched_count == 0:
                return Response(
                    {"detail": "Not enough tickets available (race condition)"},
                    status=http.HTTP_409_CONFLICT
                )

        order_inserted = orders_collection.insert_one({
            "user_id": ObjectId(request.user.id),
            "purchase_date": now(),
            "total_price": float(total),
            "discount_id": discount_doc["_id"] if discount_doc else None,
        })

        for t in tickets_data:
            tickets_collection.insert_one({
                "event_id": ObjectId(t["event"]),
                "ticket_type_id": ObjectId(t["ticket_type"]),
                "quantity": int(t["quantity"]),
                "order_id": order_inserted.inserted_id,
                "created_at": now(),
                "updated_at": now(),
            })

        created_order = orders_collection.find_one({"_id": order_inserted.inserted_id})
        return Response(order_to_api(created_order), status=http.HTTP_201_CREATED)


class NosqlOrderDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            doc = orders_collection.find_one({"_id": ObjectId(pk), "user_id": ObjectId(request.user.id)})
        except InvalidId:
            doc = None
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(order_to_api(doc))


class NosqlNotificationListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(notifications_collection.find(
            {"user_id": ObjectId(request.user.id), "is_read": False}
        ).sort("created_at", -1))
        return Response([doc_to_api(d) for d in docs])

    def post(self, request):
        ser = NotificationCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        try:
            msg = messages_collection.find_one({"_id": ObjectId(v["message_id"])})
        except InvalidId:
            msg = None
        if not msg:
            return Response({"message_id": ["Message not found"]}, status=http.HTTP_400_BAD_REQUEST)

        inserted = notifications_collection.insert_one({
            "user_id": msg["user_id"],
            "text": v["text"],
            "is_read": False,
            "created_at": now(),
            "message_id": msg["_id"],
        })
        return Response(doc_to_api(notifications_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlNotificationDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk: str):
        try:
            return notifications_collection.find_one({"_id": ObjectId(pk), "user_id": ObjectId(self.request.user.id)})
        except InvalidId:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))

    def patch(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        notifications_collection.update_one({"_id": ObjectId(pk)}, {"$set": {"is_read": True}})
        return Response({"success": True, "message": "Marked as read"})


class NosqlMessageListCreateView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(messages_collection.find({"user_id": ObjectId(request.user.id)}))
        return Response([doc_to_api(d) for d in docs])

    def post(self, request):
        ser = MessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        inserted = messages_collection.insert_one({
            "user_id": ObjectId(request.user.id),
            "text": v["text"],
            "created_at": now(),
        })
        return Response(doc_to_api(messages_collection.find_one({"_id": inserted.inserted_id})),
                        status=http.HTTP_201_CREATED)


class NosqlMessageDetailView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            doc = messages_collection.find_one({"_id": ObjectId(pk)})
        except InvalidId:
            doc = None
        if not doc:
            return Response({"detail": "Not found"}, status=http.HTTP_404_NOT_FOUND)
        return Response(doc_to_api(doc))


class NosqlMessageAllListView(APIView):
    authentication_classes = [MongoTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        docs = list(messages_collection.find({}).sort("created_at", -1))
        return Response([doc_to_api(d) for d in docs])
