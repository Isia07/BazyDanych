# # from EventTickets.shared.views import BaseRegisterView, BaseLoginView

# # class NosqlRegisterView(BaseRegisterView):
# #     database = "default"   # albo "default" jeśli default = relational

# # class NosqlLoginView(BaseLoginView):
# #     database = "default"   # albo "default"


# import bcrypt
# import jwt
# from datetime import datetime, timedelta, timezone

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions
# from django.conf import settings

# from .mongo_client import users_collection


# def make_token(user_id: str, email: str):
#     now = datetime.now(timezone.utc)
#     payload = {
#         "sub": user_id,
#         "email": email,
#         "iat": int(now.timestamp()),
#         "exp": int((now + timedelta(seconds=settings.NOSQL_JWT_EXP_SECONDS)).timestamp()),
#     }
#     return jwt.encode(payload, settings.NOSQL_JWT_SECRET, algorithm=settings.NOSQL_JWT_ALG)


# class NosqlRegisterView(APIView):
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = []  # bardzo ważne: żadnego token-auth tu

#     def post(self, request):
#         email = (request.data.get("email") or "").strip().lower()
#         password = request.data.get("password") or ""

#         if not email or not password:
#             return Response({"success": False, "error": "email and password required"}, status=400)

#         if users_collection.find_one({"email": email}):
#             return Response({"success": False, "error": "This email is already taken"}, status=400)

#         pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#         doc = {
#             "email": email,
#             "password_hash": pw_hash,
#             "name": "",
#             "surname": "",
#             "is_active": True,
#             "created_at": datetime.now(timezone.utc),
#             "updated_at": datetime.now(timezone.utc),
#         }
#         _id = users_collection.insert_one(doc).inserted_id
#         token = make_token(str(_id), email)

#         return Response({"success": True, "token": token, "user": {"id": str(_id), "email": email}}, status=201)


# class NosqlLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = []

#     def post(self, request):
#         email = (request.data.get("email") or "").strip().lower()
#         password = request.data.get("password") or ""

#         doc = users_collection.find_one({"email": email})
#         if not doc:
#             return Response({"success": False, "error": "No account found with this email"}, status=400)

#         if not doc.get("is_active", True):
#             return Response({"success": False, "error": "This account has been deactivated"}, status=400)

#         if not bcrypt.checkpw(password.encode("utf-8"), doc["password_hash"].encode("utf-8")):
#             return Response({"success": False, "error": "Incorrect password"}, status=400)

#         token = make_token(str(doc["_id"]), email)
#         return Response({"token": token, "user": {"id": str(doc["_id"]), "email": email}}, status=200)
