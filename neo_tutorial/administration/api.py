from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.response import Response
from neo_tutorial.profile.models import TutorialUser


@api_view(http_method_names=['GET'])
def profile_view(request):
    if request.user.is_anonymous:
        raise PermissionDenied

    user = TutorialUser.objects.get()

    details = {
        'id': user.id,
        'username': user.email,
        'is_manager': user.is_manager,
        'is_administrator': user.is_administrator,
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

