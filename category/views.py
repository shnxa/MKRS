from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from category import serializers
from category.models import Category


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]



# Create your views here.
