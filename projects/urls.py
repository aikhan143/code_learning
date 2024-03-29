from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

router.register('courses', CourseViewSet)
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('tasks/<slug:pk>/add_user_answer/', TaskUserViewSet.as_view({'patch': 'add_user_answer'}), name='tasks-add-user-answer'),
    path('', include(router.urls))
]

