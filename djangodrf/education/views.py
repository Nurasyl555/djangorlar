from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Min, Count, Max, Q
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, LessonMoveSerializer
from .permissions import IsCourseOwner

class CourseViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Set permissions based on the action
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsCourseOwner]
        return super().get_permissions()

    @extend_schema(
        summary="List all courses",
        parameters=[
            OpenApiParameter(name='is_active', type=bool, required=False)])
    def list(self, request):
        # only not deleted lessons
        queryset = Course.objects.all().annotate(Lessons_count=Count('lessons', filter=Q(lessons__deleted_at__isnull=True)))

        #filter by query params
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active_param.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary="Create a new course")
    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user) # Set the owner to the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(summary="get course")
    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    @extend_schema(summary="Update a course")
    def update(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course) # Check permissions

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete a course (soft delete)")
    def destroy(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course) # Check permissions
        course.soft_delete() # our custom soft delete method
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(summary="Activation course", request=None)
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course) # Check permissions
        if course.is_active:
            return Response({'detail': 'Course is already active.'}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = True
        course.save()
        return Response(CourseSerializer(course).data)
    
    @extend_schema(summary="Deactivation course", request=None)
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course) # Check permissions
        course.is_active = False
        course.save()
        return Response(CourseSerializer(course).data)
    
    @extend_schema(summary="List lessons of a course")
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        lessons = course.lessons.filter(deleted_at__isnull=True)  # only not deleted lessons
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

class LessonViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['move', 'destroy', 'publish', 'unpublish']:
            return [permissions.IsAuthenticated(), IsCourseOwner()]
        return super().get_permissions()
    
    @extend_schema(summary="Create a lesson")
    def create(self, request):
        course_id = request.data.get('course')

        if not course_id:
            return Response({'detail': "This field is required."}, status=400)
        
        course = get_object_or_404(Course, pk=course_id)
        
        # Check if the requesting user is the owner of the course
        if course.owner != request.user:
            return Response({'detail': "You do not have permission to add lessons to this course."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(summary="Move a lesson", request=LessonMoveSerializer)
    @action(detail=True, methods=['put'])
    def move(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(request, lesson)  # Check permissions

        serializer = LessonMoveSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        before_id = serializer.validated_data.get('before_lesson_id')

        if before_id is None:
            # move to the end
            max_order = Lesson.objects.filter(course=Lesson.course).aggregate(Max('order'))['order__max']
            new_order = (max_order or Decimal('0')) + Decimal('1.0')
            Lesson.indentaion = 0
        else:
            target = get_object_or_404(Lesson, pk=before_id, course=Lesson.course)
            # find previous lesson
            prev_lesson = Lesson.objects.filter(
                course=Lesson.course,
                order__lt=target.order
            ).order_by('-order').first()

            if prev_lesson:
                new_order = (prev_lesson.order + target.order) / Decimal('2.0')
            else:
                new_order = target.order - Decimal('1.0')

            Lesson.indentation = target.indentation

        Lesson.order = new_order
        Lesson.save()

        return Response({"order": Lesson.order, "indentation": Lesson.indentation})

    @extend_schema(summary="Delete a lesson (soft delete)")
    def destroy(self, request, pk=None):
        Lesson = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(request, Lesson)  # Check permissions
        Lesson.soft_delete()  # soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(summary="Publish lesson", request=None)
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(request, lesson)
        lesson.is_published = True
        lesson.save()
        return Response(LessonSerializer(lesson).data)

    @extend_schema(summary="Unpublish lesson", request=None)
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(request, lesson)
        lesson.is_published = False
        lesson.save()
        return Response(LessonSerializer(lesson).data)