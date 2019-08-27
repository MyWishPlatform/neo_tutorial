from django.urls import path, re_path
from .views import CourseListView, CourseLessonView, HomeView, CourseView
from neo_tutorial.profile.views import TutorialLoginView


urlpatterns = [
    path('', HomeView.as_view(), name='portal-home'),
    path('login/', TutorialLoginView.as_view(), name='portal-login'),
    path('courses/', CourseListView.as_view(), name='portal-courses-list'),
    path('course/<int:id>', CourseView.as_view(), name='portal-course-view'),
    path('lesson/<int:id>/', CourseLessonView.as_view(), name='portal-lesson'),
]
