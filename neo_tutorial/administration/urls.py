
from django.contrib import admin
from django.urls import path
from neo_tutorial.administration.views import AdministrationView, AdministrationLoginView

urlpatterns = [
    path('/', AdministrationView.as_view()),
    path('/login', AdministrationLoginView.as_view())
]
