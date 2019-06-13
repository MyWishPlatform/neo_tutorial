from django.views.generic.base import View, TemplateView
from django.http import HttpResponse


class AdministrationLoginView(TemplateView):

    template_name = "administration/auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdministrationView(TemplateView):

    template_name = 'administration/index.html'


