from django.forms import ModelForm
from neo_tutorial.profile.models import TutorialCommonUser


class UserForm(ModelForm):

    class Meta:
        model = TutorialCommonUser

        fields = ['username', 'password']


