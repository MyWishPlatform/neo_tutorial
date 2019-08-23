from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from neo_tutorial.profile.models import TutorialUser
from neo_tutorial.profile.api import get_password_change_url


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = TutorialUser
        fields = ('username', 'email', 'password1', 'password2')


class PortalPasswordResetForm(PasswordResetForm):

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        to_email = self.cleaned_data["email"]

        for user in self.get_users(to_email):
            current_site = request.META['HTTP_HOST']
            mail_subject = 'Password Reset'

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = get_password_change_url(request, uid, token)
            message = render_to_string('registration/password_reset_email.html', {
                'user_display': user,
                'domain':       current_site,
                'reset_link': reset_url
            })
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

