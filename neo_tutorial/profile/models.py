from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.validators import UnicodeUsernameValidator


class TutorialUserManager(auth_models.BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email or not password:
            raise ValueError('User must have a username and password')
        user_email = TutorialUserManager.normalize_email(email)
        user = self.model(
                email=user_email,
                username=user_email,
                **kwargs
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_admin = True
        user.is_staff = True
        user.save()

        return user


class TutorialUser(auth_models.AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150, unique=True, validators=[username_validator],
                                error_messages={
                                'unique': 'A user with that username already exists.'
                                },
                                )
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(null=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    is_manager = models.BooleanField('manager_status',default=False)
    is_administrator = models.BooleanField('administrator_status', default=False)

    objects = TutorialUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        ordering = ('created_on',)
        db_table = 'users'

    def __unicode__(self):
        return self.get_full_name()
