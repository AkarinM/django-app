from rest_framework import serializers
from .models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'address',
            'comment',
            'promocode',
            'created',
            'user',
            'products',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'description',
            'price',
            'discount',
            'count',
            'changed',
            'arhive',
            'created_by',
        )
