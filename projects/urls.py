from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

router.register('courses', CourseViewSet)
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('tasks/<slug:pk>/answer/', TaskViewSet.as_view({'patch': 'partial_update_user_answer'}), name='task-partial-update-user-answer'),
]

urlpatterns += router.urls