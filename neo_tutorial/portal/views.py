from django.views.generic.base import TemplateView
from neo_tutorial.courses.api import get_all_courses_details, get_lesson_details


class CourseListView(TemplateView):
    template_name = 'portal/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_list = get_all_courses_details()
        context['courses'] = course_list
        return context


class CourseLessonView(TemplateView):
    template_name = 'portal/course_lesson.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_details = get_lesson_details(id)
        context['lesson'] = lesson_details
        return context



