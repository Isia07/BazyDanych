from rest_framework import serializers
from .models import Discount, TicketType


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'code': {'validators': []},
        }

    def validate_code(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.code == value:
                return value

        if Discount.objects.using('relational').filter(code=value).exists():
            raise serializers.ValidationError("Code already exists.")
        return value

    def create(self, validated_data):
        return Discount.objects.using("relational").create(**validated_data)


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
    }

    def validate_name(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if instance.name == value:
                return value

        if TicketType.objects.using('relational').filter(name=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def create(self, validated_data):
        return TicketType.objects.using("relational").create(**validated_data)