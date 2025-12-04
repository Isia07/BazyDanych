from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from EventTickets.shared.serializers import RegisterSerializer, LoginSerializer

class BaseRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    database = 'default'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save(using=self.database)
            token, _ = Token.objects.using(self.database).get_or_create(user=user)
            return Response({
                "message": "User created",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class BaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    database = 'default'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            token, _ = Token.objects.using(self.database).get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            })
        return Response({"error": "Invalid credentials"}, status=400)