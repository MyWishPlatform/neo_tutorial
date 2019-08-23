import django.contrib.auth.views as auth_views
from rest_auth.views import LoginView as rest_LoginView
from rest_auth.views import LogoutView as rest_LogoutView

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site

from neo_tutorial.profile.models import TutorialUser
from neo_tutorial.profile.forms import SignupForm
from neo_tutorial.profile.api import user_signup_token, get_email_confirmation_url


class TutorialLoginView(auth_views.LoginView):
    pass


class TutorialLogoutView(auth_views.LogoutView):
    pass


class TutorialAPILoginView(rest_LoginView):
    pass


class TutorialAPILogoutView(rest_LogoutView):

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            logout(request)

        #response = Response({"detail": _("Successfully logged out.")},
        #                    status=status.HTTP_200_OK)
        response = HttpResponseRedirect('/')
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
               response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response


def portal_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = request.META['HTTP_HOST']
            mail_subject = 'Please Confirm Your E-mail Address'

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = user_signup_token.make_token(user)

            activate_url = get_email_confirmation_url(request, uid, token)
            message = render_to_string('profile/user_registration_email.html', {
                'user_display': user,
                'domain': current_site,
                'activate_url': activate_url
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return JsonResponse({'key': token})
    else:
        form = SignupForm()
    return render(request, 'profile/user_registration.html', {'form': form})


def portal_signup_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = TutorialUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user_signup_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect('/login')
    else:
        return JsonResponse({'error': 'Activation link is invalid'})
