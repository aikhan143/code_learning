from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Comment, Like, Rating, CartCourse, Cart
from projects.models import Course
from .serializers import CommentSerializer, LikeSerializer, RatingSerializer, CartCourseSerializer, CartSerializer

authenticated_permission = [IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = authenticated_permission

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = authenticated_permission

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = authenticated_permission
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = authenticated_permission

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by('updated_at')
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user = request.user
        course = Course.objects.get(slug=pk)

        
        cart = Cart.objects.get(user=user)
        if cart.user != user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        cart_course, course_created = CartCourse.objects.get_or_create(cart=cart, course=course)

        if not course_created:
            cart_course.quantity += 1
            cart_course.save()

        serializer = CartCourseSerializer(cart_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
