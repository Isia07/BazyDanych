from django.http import JsonResponse

from .mongo_client import (
    users_collection,
    events_collection,
    orders_collection,
    notifications_collection,
    messages_collection,
    discounts_collection,           
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .serializers import NosqlDiscountSerializer

def nosql_events_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    events = list(events_collection.find({}, {"_id": 0}))
    return JsonResponse(events, safe=False)


def nosql_users_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    users = list(users_collection.find({}, {"_id": 0}))
    return JsonResponse(users, safe=False)


def nosql_orders_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    orders = list(orders_collection.find({}, {"_id": 0}))
    return JsonResponse(orders, safe=False)


def nosql_notifications_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    notifications = list(notifications_collection.find({}, {"_id": 0}))
    return JsonResponse(notifications, safe=False)


def nosql_messages_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    messages = list(messages_collection.find({}, {"_id": 0}))
    return JsonResponse(messages, safe=False)

class NosqlDiscountListCreateView(APIView):
    def get(self, request):
        discounts = list(discounts_collection.find())
        serializer = NosqlDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlDiscountSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                NosqlDiscountSerializer(instance).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NosqlDiscountDetailView(APIView):
    def get(self, request, pk):
        try:
            obj_id = ObjectId(pk)
        except Exception:
            return Response(
                {"detail": "Nieprawidłowy identyfikator."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        discount = discounts_collection.find_one({"_id": obj_id})
        if not discount:
            return Response(
                {"detail": "Podany kod nie istnieje."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NosqlDiscountSerializer(discount)
        return Response(serializer.data)
