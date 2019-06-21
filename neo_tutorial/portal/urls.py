from django.urls import path, re_path
from .views import CourseListView, CourseLessonView, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='portal-home'),
    path('courses/', CourseListView.as_view(), name='portal-courses-list'),
    path('lesson/<int:id>/', CourseLessonView.as_view(), name='portal-lesson'),
]
