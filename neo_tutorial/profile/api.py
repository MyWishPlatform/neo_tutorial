from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.urls import reverse
from os.path import join

from neo_tutorial.settings_local import HOST_URL


class EmailConfirmTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


user_signup_token = EmailConfirmTokenGenerator()


def get_email_confirmation_url(request, uid, token):

    url = reverse('registration_email_confirm', args=[uid, token])

    if request.is_secure:
        pref = 'https://'
    else:
        pref = 'http://'

    url_base = pref + HOST_URL

    return join(url_base, url)


def get_password_change_url(request, uid, token):

    url = reverse('user_password_reset_confirm', args=[uid, token])
    return request.build_absolute_uri(url)
