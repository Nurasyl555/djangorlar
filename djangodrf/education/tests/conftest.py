import pytest
from education.models import Course, Lesson
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def course(user):
    return Course.objects.create(title='Test Course', description='A test course', owner=user)
