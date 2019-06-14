from django.urls import path
from neo_tutorial.administration.views import AdministrationView, AdministrationLoginView, UserAddView, get_all_users



urlpatterns = [
    path('', AdministrationView.as_view()),
    path('login/', AdministrationLoginView.as_view()),
    path('users/', get_all_users, name='admin-users'),
    path('users/add/', UserAddView.as_view(), name='admin-users-add'),
    path('courses/', AdministrationView.as_view(), name='admin-courses'),
    path('glossary/', AdministrationView.as_view(), name='admin-glossary'),
]
