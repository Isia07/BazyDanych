from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from EventTickets.shared.views import BaseLoginView, BaseRegisterView

from .models import Discounts, Events, Messages, Notifications, Orders, Tickets
from .serializers import (
    DiscountsSerializer,
    EventsSerializer,
    MessagesSerializer,
    NotificationsSerializer,
    OrdersSerializer,
    TicketsSerializer,
)


class RegisterView(BaseRegisterView):
    database = "objective"


class LoginView(BaseLoginView):
    database = "objective"


class DiscountsListCreateView(generics.ListCreateAPIView):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class DiscountsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        events = Events.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            return None

    def get(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response(
                {"success": False, "error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EventsSerializer(event)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response(
                {"success": False, "error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EventsSerializer(event, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response(
                {"success": False, "error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EventsSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response(
                {"success": False, "error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        event.delete()
        return Response(
            {"success": True, "message": "Event deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TicketListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tickets = Tickets.objects.select_related("event", "order", "ticket_type").all()
        serializer = TicketsSerializer(tickets, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = TicketsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserOrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Orders.objects.filter(user=request.user)
        serializer = OrdersSerializer(orders, many=True)
        return Response({"success": True, "data": serializer.data})


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = OrdersSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "success": True,
                    "data": OrdersSerializer(order, context={"request": request}).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserNotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notifications.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        serializer = NotificationsSerializer(notifications, many=True)
        return Response({"success": True, "data": serializer.data})

    def patch(self, request, pk):
        try:
            notif = Notifications.objects.get(pk=pk, user=request.user)
        except Notifications.DoesNotExist:
            return Response(
                {"success": False, "error": "Notification not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        notif.is_read = True
        notif.save()
        return Response({"success": True, "message": "Notification marked as read"})


class UserMessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = Messages.objects.filter(user=request.user).order_by("-created_at")
        serializer = MessagesSerializer(messages, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
