from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer

from neo_tutorial.profile.forms import PortalPasswordResetForm


class PortalPasswordResetSerializer(PasswordResetSerializer):
    email = serializers.EmailField()
    password_reset_form_class = PortalPasswordResetForm

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
