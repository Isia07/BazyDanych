from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework import status, generics
from .models import Discount
from .serializers import DiscountSerializer



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
        serializer.save(using="relational")

    def perform_destroy(self, instance):
        instance.delete(using="relational")

