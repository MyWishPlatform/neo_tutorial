from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ParseError
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from neo_tutorial.profile.models import TutorialUser
from neo_tutorial.courses.models import BasicCourse
from neo_tutorial.profile.api import get_full_user_statistics
from neo_tutorial.courses.api import get_course_lesson_users


@api_view(http_method_names=['GET'])
def profile_view(request):
    if request.user.is_anonymous:
        raise PermissionDenied

    request_params = request.GET
    user_id = request_params.get('id', None)

    user_object = TutorialUser.objects.get(id=user_id)

    details = {
        'id': user_object.id,
        'username': user_object.email,
        'is_manager': user_object.is_manager,
        'is_administrator': user_object.is_administrator,
        'stats': get_full_user_statistics(user_object)
    }

    return Response(details)


@api_view(http_method_names=['GET'])
def all_users_view(request):
    all_users = TutorialUser.objects.all()

    details = []
    for profile in all_users:
        details.append({
            'id': profile.id,
            'username': profile.username,
            'is_manager': profile.is_manager,
            'is_administrator': profile.is_administrator,
        })

    return Response(details)


@api_view(http_method_names=['POST'])
def create_user_view(request):
    print(request.data)
    if request.data['username'] is None:
        return ParseError('No username in request')
    else:
        username = request.data['username']

    if request.data['password'] is None:
        return ParseError('No password in request')
    else:
        pwd = request.data['password']

    is_manager = request.data['is_manager'] if 'is_manager' in request.data else False
    is_administrator = request.data['is_administrator'] if 'is_administrator' in request.data else False

    try:
        u = TutorialUser.objects.get(username=username)
        return HttpResponseBadRequest('User with username {username} already exists'.format(username=username))

    except TutorialUser.DoesNotExist:
        user = TutorialUser.objects.create_user(
            email=username,
            password=pwd,
            is_manager=is_manager,
            is_administrator=is_administrator
        )


    details = {
        'id': user.id,
        'username': user.email,
        'is_manager': user.is_manager,
        'is_administrator': user.is_administrator,
    }

    return Response(details)


@api_view(http_method_names=['GET'])
def get_user_stats(request):
    request_params = request.GET
    username = request_params.get('username', None)

    try:
        user = TutorialUser.objects.get(username=username)
    except TutorialUser.DoesNotExist:
        raise ParseError('User is not found')

    completed_statistics = get_full_user_statistics(user)
    return Response(completed_statistics)


@api_view(http_method_names=['GET'])
def get_course_stats(request):
    request_params = request.GET
    course_id = request_params.get('course_id', None)

    try:
        course = BasicCourse.objects.get(course_id=course_id)
    except BasicCourse.DoesNotExist:
        raise ParseError('Course is not found')

    completed_statistics = get_course_lesson_users(course)
    return Response(completed_statistics)
