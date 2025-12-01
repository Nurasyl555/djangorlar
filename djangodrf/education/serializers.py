from rest_framework import serializers
from .models import Course, Lesson

# Serializers for Course and Lesson models
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content', 'order',
            'indentation', 'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'order', 'course')

class CourseSerializer(serializers.ModelSerializer):
    owner =serializers.StringRelatedField() #just name user
    lessons_count = serializers.IntegerField(read_only=True) # annotated field for lessons count

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_active',
            'owner', 'created_at', 'updated_at', 'lessons_count'
        ]
        read_only_fields = ('id', 'owner' ,'created_at', 'updated_at')

class LessonMoveSerializer(serializers.Serializer):
    befor_lesson_id = serializers.IntegerField(required=False, allow_null=True)