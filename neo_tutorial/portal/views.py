from django.views.generic.base import TemplateView
from neo_tutorial.courses.api import get_all_courses_details, get_lesson_details, get_speciality_by_id, \
    get_courses_details
from neo_tutorial.courses.models import BasicCourse


class HomeView(TemplateView):
    template_name = 'portal/home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course_list = get_all_courses_details()
#         context['courses'] = course_list
#         return context


class CourseListView(TemplateView):
    template_name = 'portal/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_courses = BasicCourse.objects.filter(is_active=True).order_by('-updated_at')

        filter_tag = self.request.GET.get('q')
        if filter_tag is not None:
            active_courses = active_courses.filter(tags__contains=[filter_tag])
            context['selected_tag'] = filter_tag

        filter_spec = self.request.GET.get('spec')
        if filter_spec is not None:
            active_courses = active_courses.filter(speciality_id=filter_spec)
            context['selected_spec'] = filter_spec

        course_list = get_courses_details(active_courses)
        context['courses'] = course_list

        active_specialities_id = []
        for course in active_courses:
            speciality_id = course.speciality_id
            if speciality_id not in active_specialities_id:
                active_specialities_id.append(course.speciality_id)

        active_specialities = []
        for spec_id in active_specialities_id:
            active_specialities.append(get_speciality_by_id(spec_id))
        context['speciality_list'] = active_specialities
        return context


class CourseLessonView(TemplateView):
    template_name = 'portal/course_lesson.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_details = get_lesson_details(id)
        context['lesson'] = lesson_details
        return context


class CourseView(TemplateView):
    template_name= 'portal/course.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        course_q = BasicCourse.objects.filter(id=id)
        course_details = get_courses_details(course_q)[0]
        context['course'] = course_details

        lessons = course_q.first().lesson_set.all().order_by('id')

        lessons_details = []
        for lesson in lessons:
            details = get_lesson_details(lesson.id, detail_contents=False)
            lessons_details.append(details)

        context['lessons'] = lessons_details
        return context;