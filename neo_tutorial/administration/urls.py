from django.urls import path
from neo_tutorial.administration.views import AdministrationView, AdministrationLoginView, UserListView, UserAddView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', AdministrationView.as_view()),
    path('login/', AdministrationLoginView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/add', UserAddView.as_view()),

]
