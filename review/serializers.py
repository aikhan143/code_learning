from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from projects.serializers import CourseSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['course'] = instance.course.title
        return res
    
    def create(self, validated_data):
        user = self.context.get('request').user
        course_slug = self.context['view'].kwargs.get('slug')

        course = get_object_or_404(Course, slug=course_slug)

        validated_data['course'] = course

        comment = Comment.objects.create(user=user, **validated_data)
        return comment

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_product(self, course):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(course=course, user=user).exists():
            raise serializers.ValidationError('You have liked this post already')
        return course    

    def create(self, validated_data):
        user = self.context.get('request').user
        course_slug = self.context['view'].kwargs.get('slug')

        course = get_object_or_404(Course, slug=course_slug)

        validated_data['course'] = course
        like = Like.objects.create(user=user, **validated_data)
        return like


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        course_slug = self.context['view'].kwargs.get('slug')

        course = get_object_or_404(Course, slug=course_slug)

        validated_data['course'] = course
        rating = Rating.objects.create(user=user, **validated_data)
        return rating

class CartCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CartCourse
        fields = ['course', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_courses = CartCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'updated_at', 'cart_courses']
