from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import *
from .serializers import *
from cart.permissions import IsPaidPermission

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

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course']
    search_fields = ['title']

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return ProjectListSerializer
        else:
            return ProjectSerializer
        
    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permissions = [IsPaidPermission]
        else:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]
        
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]

class TaskUserViewSet(ModelViewSet):
    serializer_class = TaskUserSerializer
    queryset = TaskUser.objects.all()
    @action(detail=True, methods=['patch'], serializer_class=TaskUserSerializer, permission_classes=[IsPaidPermission])
    def add_user_answer(self, request, pk=None):
        user = request.user
        task = Task.objects.get(slug=pk)
        task_user, created = TaskUser.objects.get_or_create(user=user, task=task)

        task_user.user_answer = request.data.get('user_answer')
        task_user.save()
        serializer = TaskUserSerializer(task_user)

        if task.correct_answer == task_user.user_answer:
            task_user.status = 'D'
            return Response(serializer.data, status=201)
        raise ValidationError('Incorrect answer.')
