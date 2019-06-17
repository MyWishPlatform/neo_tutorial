from django.urls import path, re_path
from neo_tutorial.administration.views import AdministrationView, TutorialAdminLoginView, TutorialAdminLogoutView

from neo_tutorial.administration.api import profile_view, all_users_view, create_user_view
from neo_tutorial.courses.views import all_courses_view, create_course_view, update_course_view


urlpatterns = [
    path('login/', TutorialAdminLoginView.as_view()),
    path('logout/', TutorialAdminLogoutView.as_view(), name='profile-logout'),


#     path('users/create/', UserAddView.as_view(), name='admin-users-create'),
#     path('users/preview/', UserPreview.as_view(), name='admin-users-preview'),


#     path('courses/', get_all_courses, name='admin-courses'),
#     path('glossary/', AdministrationView.as_view(), name='admin-glossary'),

    path('api/users/', all_users_view, name='api-admin-all-users'),
    path('api/users/create/', create_user_view, name='api-admin-users-create'),
    path('api/users/preview/', profile_view, name='api-admin-users-preview'),
    path('api/courses/', all_courses_view, name='api-admin-all-courses'),
    path('api/courses/create/', create_course_view, name='api-admin-courses-create'),
    path('api/courses/update/', update_course_view, name='api-admin-courses-update'),


    re_path(r'^(.*)$', AdministrationView.as_view()),
]
