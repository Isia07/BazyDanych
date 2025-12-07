from rest_framework import serializers
from .models import Discount

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'code': {'validators': []},
        }

    def validate_code(self, value):
        if Discount.objects.using('relational').filter(code=value).exists():
            raise serializers.ValidationError("Kod rabatowy o podanej wartości już istnieje.")
        return value

    def create(self, validated_data):
        return Discount.objects.using("relational").create(**validated_data)