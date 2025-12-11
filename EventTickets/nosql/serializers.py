from rest_framework import serializers
from bson import ObjectId

from .mongo_client import (
    discounts_collection,
    event_types_collection,
    seat_types_collection,
    ticket_types_collection,
    statuses_collection,
    events_collection,
)


class NosqlDiscountSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    discount_percentage = serializers.FloatField()
    code = serializers.CharField(max_length=50)
    valid_from = serializers.DateTimeField()
    valid_to = serializers.DateTimeField()

    def to_representation(self, instance):
        if isinstance(instance, dict):
            data = instance.copy()
            if "_id" in data:
                data["id"] = str(data.pop("_id"))
            return data
        return super().to_representation(instance)

    def validate_code(self, value):
        existing = discounts_collection.find_one({"code": value})
        if existing:
            raise serializers.ValidationError(
                "Kod rabatowy o podanej wartości już istnieje."
            )
        return value

    def create(self, validated_data):
        result = discounts_collection.insert_one(validated_data)
        validated_data["id"] = float(validated_data["discount_percentage"])
        return validated_data

class NosqlEventTypeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        result = event_types_collection.insert_one(validated_data)
        validated_data["id"] = str(result.inserted_id)
        return validated_data


class NosqlSeatTypeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        result = seat_types_collection.insert_one(validated_data)
        validated_data["id"] = str(result.inserted_id)
        return validated_data


class NosqlTicketTypeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        result = ticket_types_collection.insert_one(validated_data)
        validated_data["id"] = str(result.inserted_id)
        return validated_data


class NosqlStatusSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        result = statuses_collection.insert_one(validated_data)
        validated_data["id"] = str(result.inserted_id)
        return validated_data
    
class NosqlEventSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    localization = serializers.CharField()
    event_type = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()

    tickets = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    def create(self, validated_data):
        from datetime import datetime

        now = datetime.utcnow()
        validated_data.setdefault("tickets", [])
        validated_data["created_at"] = now
        validated_data["updated_at"] = now

        result = events_collection.insert_one(validated_data)
        validated_data["id"] = str(result.inserted_id)
        return validated_data