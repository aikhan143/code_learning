from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']

class ProjectViewSet(PermissionMixin, ModelViewSet):
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course']
    search_fields = ['title']

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return ProjectListSerializer
        else:
            return ProjectSerializer
        
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskSerializer
        else:
            return TaskUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permissions = [AllowAny]
        elif self.action == 'create':
            permissions = [IsPaidPermission]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]