from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from EventTickets.shared.models import User
from EventTickets.shared.serializers import RegisterSerializer, LoginSerializer


class BaseRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    database = 'default'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user.save(using=self.database)
                token, _ = Token.objects.using(self.database).get_or_create(user=user)
                return Response({
                    "success": True
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    "success": False,
                    "error": "This email is already taken"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class BaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    database = 'default'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.using(self.database).get(email=email)

            if not user.is_active:
                return Response({
                    "success": False,
                    "error": "This account has been deactivated"
                }, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                token, _ = Token.objects.using(self.database).get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name or "",
                        "surname": user.surname or "",
                        "role": user.role
                    }
                }, status=200)
            else:
                return Response({
                    "success": False,
                    "error": "Incorrect password"
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": "No account found with this email"
            }, status=status.HTTP_400_BAD_REQUEST)