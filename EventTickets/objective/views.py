from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from EventTickets.shared.views import BaseLoginView, BaseRegisterView

from .models import (
    Discounts,
    Events,
    EventTypes,
    Messages,
    Notifications,
    Orders,
    Status,
    Tickets,
    TicketTypes,
)
from .serializers import (
    DiscountsSerializer,
    EventsSerializer,
    EventTypesSerializer,
    MessagesSerializer,
    NotificationsSerializer,
    OrdersSerializer,
    StatusSerializer,
    TicketsSerializer,
    TicketTypesSerializer,
)


class ObjectiveTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.using("objective").select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        return (token.user, token)


class ObjectiveTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.using("objective").select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        return (token.user, token)


class RegisterView(BaseRegisterView):
    database = "objective"


class LoginView(BaseLoginView):
    database = "objective"


class DiscountsListCreateView(generics.ListCreateAPIView):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class DiscountsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer
    lookup_field = "id"
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    lookup_field = "pk"
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Tickets.objects.select_related("event", "order", "ticket_type").all()
    serializer_class = TicketsSerializer
    authentication_classes = [ObjectiveTokenAuthentication]
    permission_classes = [permissions.AllowAny]


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrdersSerializer
    authentication_classes = [ObjectiveTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrdersSerializer
    authentication_classes = [ObjectiveTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserNotificationListView(APIView):
    authentication_classes = [ObjectiveTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        notifications = Notifications.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            notif = Notifications.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({"success": True, "message": "Notification marked as read"})
        except Notifications.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessagesSerializer
    authentication_classes = [ObjectiveTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Messages.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class StatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    lookup_field = "pk"
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class EventTypeListCreateView(generics.ListCreateAPIView):
    queryset = EventTypes.objects.all()
    serializer_class = EventTypesSerializer
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class EventTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventTypes.objects.all()
    serializer_class = EventTypesSerializer
    lookup_field = "pk"
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class TicketTypeListCreateView(generics.ListCreateAPIView):
    queryset = TicketTypes.objects.all()
    serializer_class = TicketTypesSerializer
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]


class TicketTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketTypes.objects.all()
    serializer_class = TicketTypesSerializer
    lookup_field = "pk"
    authentication_classes = [ObjectiveTokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]
