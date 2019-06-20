from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from neo_tutorial.profile.views import TutorialLoginView, TutorialLogoutView


class TutorialAdminLoginView(TutorialLoginView):
    template_name = 'administration/auth.html'
    next = '/administration/'

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
            return HttpResponseRedirect(self.next)
        else:
            return HttpResponseForbidden()


class TutorialAdminLogoutView(TutorialLogoutView):
    template_name = 'administration/auth.html'
    next_page = '/administration/login/'


class AdministrationView(TemplateView):
    template_name = 'administration/index.html'
    user = None

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/administration/login/')

        self.user = request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context
