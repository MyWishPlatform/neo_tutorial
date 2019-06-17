from django.forms import ModelForm
from neo_tutorial.profile.models import TutorialUser
from neo_tutorial.courses.models import BasicCourse


class UserForm(ModelForm):
    class Meta:
        model = TutorialUser
        fields = ['email', 'username', 'password', 'is_manager', 'is_administrator']


class CourseForm(ModelForm):
    class Meta:
        model = BasicCourse
        fields = ['name']

