from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

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

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskSerializer
        else:
            return TaskUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list', 'create'):
            permissions = [AllowAny]
        else:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]