from django.urls import path, re_path
from neo_tutorial.administration.views import AdministrationView, TutorialAdminLoginView, TutorialAdminLogoutView

from neo_tutorial.administration.api import profile_view, all_users_view, create_user_view
from neo_tutorial.courses.views import all_courses_view, create_course_view, update_course_view, \
    get_course_view, get_courses_by_tag_view, get_specialities_view, create_lesson_view, get_lessons_by_course_view,\
    upload_lesson_images_view, edit_lesson_content_view, delete_lesson_view


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
    path('api/courses/preview/',get_course_view, name='api-admin-courses-preview'),
    path('api/courses/by_tag/', get_courses_by_tag_view, name='api-admin-courses-by-tag'),
    path('api/courses/specialities/', get_specialities_view, name='api-admin-courses-specialities'),
    path('api/lessons/create/', create_lesson_view, name='api-admin-lessons-create'),
    path('api/lessons/by_course_id/', get_lessons_by_course_view, name='api-admin-lessons-by-course-id'),
    path('api/lessons/upload_images/', upload_lesson_images_view, name='api-admin-lessons-upload-images'),
    path('api/lessons/edit_content/', edit_lesson_content_view, name='api-admin-lessons-edit-content'),
    path('api/lessons/delete/', delete_lesson_view, name='api-admin-lessons-delete'),


    re_path(r'^(.*)$', AdministrationView.as_view()),
]
