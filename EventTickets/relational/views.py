from EventTickets.shared.views import BaseRegisterView, BaseLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Discount
from .serializers import DiscountSerializer



class RelRegisterView(BaseRegisterView):
    database = 'relational'


class RelLoginView(BaseLoginView):
    database = 'relational'


class DiscountListCreateView(APIView):
    def get(self, request):
        discounts = Discount.objects.using("relational").all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetailView(APIView):
    def get(self, request, pk):
        try:
            discount = Discount.objects.using("relational").get(pk=pk)
        except Discount.DoesNotExist:
            return Response({"detail": "Podany kod nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
