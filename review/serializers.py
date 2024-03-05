from rest_framework import serializers

from .models import *

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['course'] = instance.course.title
        return res


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['like', 'course']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['course'] = instance.course.title
        if instance.like is True:
            res['like'] = 'Liked'
        else:
            res['like'] = 'Disliked'
        return res


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    course = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ['rating', 'course']

