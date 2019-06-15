from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden

from neo_tutorial.profile.models import TutorialUser
from neo_tutorial.profile.views import TutorialLoginView, TutorialAPILoginView
from .forms import UserForm


class TutorialAdminLoginView(TutorialLoginView):
    template_name = 'administration/auth.html'
    success_url = '/administration/'

    def __init__(self):
        self.profile = None
        super().__init__()

    def check_privileges(self):
        if self.profile.is_manager or self.profile.is_administrator:
            return True

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        self.profile = user

        # Check here if the user is an admin
        print(self.check_privileges())
        if user is not None and user.is_active and self.check_privileges():
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseForbidden()


#class AdministrationLoginView(LoginView):
#    template_name = "administration/auth.html"
#    success_url = "administration"


class AdministrationView(TemplateView):
    template_name = 'administration/index.html'


class UserListView(FormView):
    form_class = UserForm
    template_name = "administration/userlist.html"


class UserAddView(CreateView):
    form_class = UserForm
    template_name = "administration/useradd.html"

    success_url = "/administration/users/preview/"

    def get_success_url(self):
        print(self.object.id)

        return reverse('admin-users-preview', kwargs=[self.object.id])


#        messages.add_message(self.request, messages.SUCCESS, 'User created!')
#        return reverse('admin-users-add')


class UserPreview(UpdateView):
    model = TutorialUser
    form_class = UserForm
    template_name = "administration/userpreview.html"

    def get(self, request, *args, **kwargs):
        self.object = TutorialUser.objects.get(id=self.kwargs['id'])
        return super().get(request, *args, **kwargs)


def get_all_users(request):
    user_list = TutorialUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'administration/userlist.html', context)
