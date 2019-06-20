from django.urls import path, re_path
from .views import CourseListView


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='portal-courses-list')
]
