from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import IsPaidPermission

class PermissionMixin:
    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permissions = [AllowAny]
        else:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]
    
class CourseViewSet(PermissionMixin, ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ProjectViewSet(PermissionMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']

class TaskViewSet(PermissionMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'], permission_classes=[IsPaidPermission])
    def partial_update_user_answer(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)