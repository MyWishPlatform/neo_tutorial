from django.views.generic.base import View, TemplateView
from django.http import HttpResponse


class ProfileLoginView(TemplateView):

    template_name = 'index.html'




class ProfileView(TemplateView):

    template_name = 'index.html'
