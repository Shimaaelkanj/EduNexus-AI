from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'filename', 'content', 'summary', 'simple_summary', 'outline', 'created_at']
        read_only_fields = ['id', 'created_at']