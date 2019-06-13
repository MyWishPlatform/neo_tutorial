from django.views.generic import DetailView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.forms import modelformset_factory
from neo_tutorial.profile.models import TutorialCommonUser
from neo_tutorial.administration.forms import UserForm
from neo_tutorial.administration.api import get_all_users


class AdministrationLoginView(LoginView):
    template_name = "administration/auth.html"


class AdministrationView(TemplateView):

    template_name = 'administration/index.html'


class UserListView(DetailView):
    model = TutorialCommonUser
    template_name = "administration/userlist.html"



class UserAddView(FormView):
    form_class = UserForm
    template_name = "administration/useradd.html"

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'User created!')
        return reverse('user-add')
