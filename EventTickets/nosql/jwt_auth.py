import jwt
from bson import ObjectId
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from .mongo_client import users_collection


class MongoUser:
    def __init__(self, _id: str, email: str, is_active: bool = True):
        self.id = _id              # string ObjectId
        self.email = email
        self.is_active = is_active

    @property
    def is_authenticated(self):
        return True


class MongoJWTAuthentication(BaseAuthentication):
    """
    Authorization: Bearer <jwt>
    """
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid auth header (use Bearer <token>).")

        token = parts[1]
        try:
            payload = jwt.decode(token, settings.NOSQL_JWT_SECRET, algorithms=[settings.NOSQL_JWT_ALG])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationFailed("Invalid token payload.")

        try:
            oid = ObjectId(user_id)
        except Exception:
            raise AuthenticationFailed("Invalid user id.")

        doc = users_collection.find_one({"_id": oid})
        if not doc:
            raise AuthenticationFailed("User not found.")
        if not doc.get("is_active", True):
            raise AuthenticationFailed("User inactive.")

        return (MongoUser(str(doc["_id"]), doc["email"], True), token)
