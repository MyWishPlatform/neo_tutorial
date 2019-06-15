from django.forms import ModelForm
from neo_tutorial.profile.models import TutorialUser



class UserForm(ModelForm):

    class Meta:
        model = TutorialUser
        fields = ['email', 'username', 'password', 'is_manager', 'is_administrator']


