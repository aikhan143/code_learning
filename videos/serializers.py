from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['email', 'name', 'file']

    def create(self, validated_data):
        email = validated_data['email']
        resume, created = Resume.objects.get_or_create(email=email, defaults=validated_data)
        if not created:
            pass
        return resume

