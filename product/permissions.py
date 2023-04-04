from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
