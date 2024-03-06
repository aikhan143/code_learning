from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['title', 'price']

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'course']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = TaskUser
        fields = '__all__'

    
    def validate(self, attrs):
        task = attrs.get('task')
        user_answer = attrs.get('user_answer')

        if user_answer == task.correct_answer:
            attrs['status'] = 'D'
            return attrs
        raise serializers.ValidationError('Incorrect answer. Try again.')

    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        user_answer = validated_data.pop('user_answer')
        task = TaskUser.objects.create(user=user, user_answer=user_answer, **validated_data)
        return task