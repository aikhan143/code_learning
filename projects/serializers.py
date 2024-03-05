from rest_framework import serializers
from .models import *
import stripe
import os
from dotenv import load_dotenv

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class CourseSerializer(serializers.ModelSerializer):

    status = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'price']

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description']

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title', 'description', 'user_answer']

    def validate_user_answer(self, user_answer):
        task = Task.objects.filter(user_answer=user_answer).first()
        if task and task.is_user_answer_correct():
            return 'Your answer if correct'
        return 'Incorrect answer. Try again.'