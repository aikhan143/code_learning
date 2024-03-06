from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

router.register('courses', CourseViewSet)
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls))
]

