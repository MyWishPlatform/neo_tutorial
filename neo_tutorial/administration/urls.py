from django.urls import path
from neo_tutorial.administration.views import AdministrationView, AdministrationLoginView, UserAddView, get_all_users



urlpatterns = [
    path('', AdministrationView.as_view()),
    path('login/', AdministrationLoginView.as_view()),
    path('users/', get_all_users),
    path('users/add/', UserAddView.as_view())
]
