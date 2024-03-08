from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

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

    def create(self, validated_data):
        user = self.context.get('request').user
        course_slug = self.context['view'].kwargs.get('slug')

        course = get_object_or_404(Course, slug=course_slug)

        if Like.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('You have liked this course already')

        validated_data['course'] = course
        like = Like.objects.create(user=user, **validated_data)
        return like

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        course_slug = self.context['view'].kwargs.get('slug')

        course = get_object_or_404(Course, slug=course_slug)

        if Rating.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('You have rated this course already')

        validated_data['course'] = course
        rating = Rating.objects.create(user=user, **validated_data)
        return rating
