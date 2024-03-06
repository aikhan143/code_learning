from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
  
router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comment')
router.register('likes', LikeViewSet, basename='like')
router.register('ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
