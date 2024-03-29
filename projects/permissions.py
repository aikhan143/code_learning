from rest_framework.permissions import BasePermission 

class IsPaidPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_paid and obj.is_paid