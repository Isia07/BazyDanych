import secrets
from datetime import datetime, timezone as dt_tz

from bson import ObjectId
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .mongo_client import users_collection, tokens_collection



class MongoUser:
    """
    Minimalny obiekt usera dla DRF permissions.IsAuthenticated itd.
    """
    def __init__(self, user_oid: ObjectId, email: str, is_active: bool = True):
        self.id = str(user_oid)     # string ObjectId
        self.email = email
        self.is_active = is_active

    @property
    def is_authenticated(self):
        return True


class MongoTokenAuthentication(BaseAuthentication):
    """
    Obsługuje nagłówek:
      Authorization: Token <key>
    gdzie <key> jest kluczem z kolekcji tokens.
    """
    keyword = "Token"

    def authenticate(self, request):
        auth = get_authorization_header(request).decode("utf-8")
        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None  # pozwól innym auth (dla innych baz)

        key = parts[1].strip()
        token_doc = tokens_collection.find_one({"_id": key})
        if not token_doc:
            raise AuthenticationFailed("Invalid token.")

        user_oid = token_doc.get("user_id")
        if not isinstance(user_oid, ObjectId):
            raise AuthenticationFailed("Invalid token user reference.")

        user_doc = users_collection.find_one({"_id": user_oid})
        if not user_doc:
            raise AuthenticationFailed("User not found.")
        if not user_doc.get("is_active", True):
            raise AuthenticationFailed("User inactive.")

        return (MongoUser(user_oid, user_doc.get("email", ""), True), key)
