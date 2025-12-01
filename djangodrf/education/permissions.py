from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a course to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the course
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'course'):
            # If the object is a lesson, check the course owner
            return obj.course.owner == request.user
        return False