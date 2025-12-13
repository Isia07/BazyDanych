from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import (
    Event, Ticket, Order, OrderTicket, Notification, Message,
    StatusObj, EventTypeObj, TicketTypeObj, SeatTypeObj, DiscountObj
)
from .serializers import (
    EventSerializer, TicketSerializer, OrderSerializer,
    OrderTicketSerializer, NotificationSerializer, MessageSerializer,
    StatusObjSerializer, EventTypeObjSerializer, TicketTypeObjSerializer,
    SeatTypeObjSerializer, DiscountObjSerializer
)


class RegisterView(BaseRegisterView):
    database = 'objective_relational'


class LoginView(BaseLoginView):
    database = 'objective_relational'


class StatusObjListCreateView(generics.ListCreateAPIView):
    queryset = StatusObj.objects.all()
    serializer_class = StatusObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class StatusObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StatusObj.objects.all()
    serializer_class = StatusObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EventTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = EventTypeObj.objects.all()
    serializer_class = EventTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class EventTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventTypeObj.objects.all()
    serializer_class = EventTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class TicketTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = TicketTypeObj.objects.all()
    serializer_class = TicketTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class TicketTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketTypeObj.objects.all()
    serializer_class = TicketTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class SeatTypeObjListCreateView(generics.ListCreateAPIView):
    queryset = SeatTypeObj.objects.all()
    serializer_class = SeatTypeObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class SeatTypeObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeatTypeObj.objects.all()
    serializer_class = SeatTypeObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class DiscountObjListCreateView(generics.ListCreateAPIView):
    queryset = DiscountObj.objects.all()
    serializer_class = DiscountObjSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class DiscountObjDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscountObj.objects.all()
    serializer_class = DiscountObjSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        events = Event.objects.select_related('event_type', 'status').all()
        serializer = EventSerializer(events, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.select_related('event_type', 'status').get(pk=pk)
        except Event.DoesNotExist:
            return None

    def get(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return Response({"success": False, "error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response({"success": True, "message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TicketListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.select_related('event', 'discount').all()
        serializer = TicketSerializer(tickets, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserOrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('orderticket_set__ticket_types',
                                                                          'orderticket_set__seat_type')
        serializer = OrderSerializer(orders, many=True)
        return Response({"success": True, "data": serializer.data})


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = OrderSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "data": OrderSerializer(order, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserNotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response({"success": True, "data": serializer.data})

    def patch(self, request, pk):
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({"success": False, "error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        notif.is_read = True
        notif.save()
        return Response({"success": True, "message": "Notification marked as read"})


class UserMessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(user=request.user).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
