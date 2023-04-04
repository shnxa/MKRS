from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from rating.serializers import RatingSerializer
from .models import Product
from . import serializers
from .permissions import IsOwner


User = get_user_model()

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.IsAuthenticatedOrReadOnly()]


    # /api/v1/products/id/ratings/
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user


        if self.request.method == "GET":
            ratings = product.ratings.all()
            serializer = RatingSerializer(instance=ratings, many=True).data
            return response.Response(serializer, status=200)

        elif self.request.method == "POST":
            if product.ratings.filter(owner=user).exists():
                return response.Response('You\'ve already rated this product!', status=400)

            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return response.Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return response.Response('You never rated this product!', status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            return response.Response('Successfully deleted!', status=204)