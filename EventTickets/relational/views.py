from django.shortcuts import render
from rest_framework import generics
from EventTickets.relational.models import Discount
from EventTickets.relational.serializers import DiscountSerializer
from EventTickets.shared.views import BaseRegisterView, BaseLoginView

class RelRegisterView(BaseRegisterView):
    database = 'relational'


class RelLoginView(BaseLoginView):
    database = 'relational'


class DiscountListCreateView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountDetailView(generics.RetrieveAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

