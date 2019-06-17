import django.contrib.auth.views as auth_views
from rest_auth.views import LoginView as rest_LoginView


class TutorialLoginView(auth_views.LoginView):
    pass


class TutorialLogoutView(auth_views.LogoutView):
    pass


class TutorialAPILoginView(rest_LoginView):
    pass
