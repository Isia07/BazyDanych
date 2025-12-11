from django.http import JsonResponse

from .mongo_client import (
    users_collection,
    events_collection,
    orders_collection,
    notifications_collection,
    messages_collection,
    discounts_collection,
    event_types_collection,
    seat_types_collection,
    ticket_types_collection,
    statuses_collection,    
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .serializers import (
    NosqlDiscountSerializer,
    NosqlDiscountSerializer,
    NosqlEventTypeSerializer,
    NosqlSeatTypeSerializer,
    NosqlTicketTypeSerializer,
    NosqlStatusSerializer,
    NosqlEventSerializer,
)

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

class NosqlEventTypeListCreateView(APIView):
    def get(self, request):
        docs = list(event_types_collection.find())
        for d in docs:
            d["id"] = str(d.pop("_id"))
        serializer = NosqlEventTypeSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlEventTypeSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(NosqlEventTypeSerializer(instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NosqlSeatTypeListCreateView(APIView):
    def get(self, request):
        docs = list(seat_types_collection.find())
        for d in docs:
            d["id"] = str(d.pop("_id"))
        serializer = NosqlSeatTypeSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlSeatTypeSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(NosqlSeatTypeSerializer(instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NosqlTicketTypeListCreateView(APIView):
    def get(self, request):
        docs = list(ticket_types_collection.find())
        for d in docs:
            d["id"] = str(d.pop("_id"))
        serializer = NosqlTicketTypeSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlTicketTypeSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(NosqlTicketTypeSerializer(instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NosqlStatusListCreateView(APIView):
    def get(self, request):
        docs = list(statuses_collection.find())
        for d in docs:
            d["id"] = str(d.pop("_id"))
        serializer = NosqlStatusSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlStatusSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(NosqlStatusSerializer(instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NosqlEventListCreateView(APIView):
    def get(self, request):
        docs = list(events_collection.find())
        for d in docs:
            d["id"] = str(d.pop("_id"))
        serializer = NosqlEventSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NosqlEventSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(NosqlEventSerializer(instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)