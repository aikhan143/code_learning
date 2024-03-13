from rest_framework import serializers
from django.db.models import Avg
from .models import *
from review.serializers import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get('request').user
        if not user.is_staff:
            representation.pop('correct_answer', None)
        return representation

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title']

class TaskUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = TaskUser
        fields = '__all__'
    
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tasks'] = TaskListSerializer(instance.tasks.all(), many=True).data
        return representation
    
class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'price']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['projects'] = ProjectListSerializer(instance.projects.all(), many=True).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        return representation
