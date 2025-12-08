from rest_framework import serializers
from bson import ObjectId

from .mongo_client import discounts_collection


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
