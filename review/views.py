from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Like, Rating
from .serializers import CommentSerializer, LikeSerializer, RatingSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
