from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render

from neo_tutorial.administration.forms import UserForm

from neo_tutorial.profile.models import TutorialCommonUser


class AdministrationLoginView(LoginView):
    template_name = "administration/auth.html"


class AdministrationView(TemplateView):

    template_name = 'administration/index.html'


class UserListView(FormView):
    form_class = UserForm
    template_name = "administration/userlist.html"


class UserAddView(FormView):
    form_class = UserForm
    template_name = "administration/useradd.html"

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'User created!')
        return reverse('user-add')


def get_all_users(request):
    user_list = TutorialCommonUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'administration/userlist.html', context)
