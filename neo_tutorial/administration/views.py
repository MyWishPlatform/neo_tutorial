from django.views.generic.base import View, TemplateView
from django.http import HttpResponse


class AdministrationLoginView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdministrationView(TemplateView):

    template_name = 'index.html'


