from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient 
from education.models import Course, Lesson
from decimal import Decimal

# Test auth token retrieval
@pytest.mark.django_db
def test_auth_token(api_client: APIClient, user: User):
    # Good data
    response = api_client.post('/education/token/', {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
    assert 'access' in response.data
    # Bad data
    response = api_client.post('/education/token/', {'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 401

# TEST COURSE
@pytest.mark.django_db
def test_course_endpoints(api_client: APIClient, user: User, course: Course):
    api_client.force_authenticate(user=user)
    # good  
    response = api_client.get('/education/v1/education/courses/')
    assert response.status_code == 200
    assert len(response.data) == 1
    # bad
    api_client.logout()
    response = api_client.post('/education/v1/education/courses/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_course(api_client: APIClient, user: User):
    api_client.force_authenticate(user=user)
    # good
    response = api_client.post('/education/v1/education/courses/', {'title': 'New Course', 'description': 'Course description'})
    assert response.status_code == 201
    assert response.data['owner'] == user.username
    # bad
    response = api_client.post('/education/v1/education/courses/', {})
    assert response.status_code == 400

@pytest.mark.django_db
def test_delete_course(api_client: APIClient, user: User, course: Course):
    api_client.force_authenticate(user=user)
    # good
    response = api_client.delete(f'/education/v1/education/courses/{course.id}/')
    assert response.status_code == 204
    course.refresh_from_db()
    assert course.deleted_at is not None
    # bad
    response = api_client.delete(f'/education/v1/education/courses/999/')
    assert response.status_code == 404

# TEST LESSON
@pytest.mark.django_db
def test_create_lesson(api_client: APIClient, user: User, course: Course):
    api_client.force_authenticate(user=user)
    # good
    response = api_client.post('/education/v1/education/lessons/', {
        'course': course.id,
        'title': 'New Lesson',
        'content': 'Lesson content'
    })
    assert response.status_code == 201
    assert response.data['course'] == course.id
    # bad - missing course
    response = api_client.post('/education/v1/education/lessons/', {
        'title': 'New Lesson',
        'content': 'Lesson content'
    })
    assert response.status_code == 400

