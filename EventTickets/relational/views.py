from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework import status, generics
from .models import Discount, TicketType
from .serializers import DiscountSerializer, TicketTypeSerializer


class RelRegisterView(BaseRegisterView):
    database = 'relational'


class RelLoginView(BaseLoginView):
    database = 'relational'


class RelDiscountListCreateView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()


class RelDiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")

class RelTicketTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketTypeSerializer

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_create(self, serializer):
        serializer.save()

class RelTicketTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeSerializer

    def get_queryset(self):
        return TicketType.objects.using("relational").all()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(using="relational")
