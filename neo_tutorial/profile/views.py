from django.contrib.auth.views import LoginView as auth_LoginView
from rest_auth.views import LoginView as rest_LoginView


class TutorialLoginView(auth_LoginView):
    pass


class TutorialAPILoginView(rest_LoginView):
    pass
