from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Product
        fields = ('owner', 'owner_email', ' title', 'price', 'image', 'stock')


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Product
        fields = "__all__"