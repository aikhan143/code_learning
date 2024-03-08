from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
  
urlpatterns = [
    path('courses/<slug:slug>/comments/', CommentViewSet.as_view({'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment-create'),
    path('courses/<slug:slug>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('courses/<slug:slug>/dislike/', LikeViewSet.as_view({'delete': 'destroy'}), name='like-destroy'),
    path('courses/<slug:slug>/rating/', RatingViewSet.as_view({'post': 'create'}), name='like-create'),
]
