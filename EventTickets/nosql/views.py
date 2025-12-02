from django.shortcuts import render
from django.http import JsonResponse
from .mongo_client import (
    users_collection,
    events_collection,
    orders_collection,
    notifications_collection,
    messages_collection,
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
