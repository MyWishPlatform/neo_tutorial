from django.views.generic.base import TemplateView
from neo_tutorial.courses.api import get_all_courses_details, get_lesson_details, get_speciality_by_id, \
    get_courses_details
from neo_tutorial.courses.models import BasicCourse, Lesson


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
        active_courses = BasicCourse.objects.filter(is_active=True, lng='en').order_by('-updated_at')
        all_active_courses = active_courses

        filter_tag = self.request.GET.get('q')
        if filter_tag is not None:
            active_courses = active_courses.filter(tags__contains=[filter_tag])
            context['selected_tag'] = filter_tag

        filter_spec = self.request.GET.get('spec')
        if filter_spec is not None:
            active_courses = active_courses.filter(speciality_id=filter_spec)
            context['selected_spec'] = int(filter_spec)

        course_list = get_courses_details(active_courses)
        for course in course_list:
            other_lang_courses = BasicCourse.objects.filter(course_id=course['course_id'], is_active=True)

            internal_ids = {}
            for course_other_lang in other_lang_courses:
                lessons_count = len(Lesson.objects.filter(course=course_other_lang).order_by('order'))
                if lessons_count > 0:
                    internal_ids[course_other_lang.lng] = course_other_lang.id

            course['other_lang_ids'] = internal_ids

        context['courses'] = course_list

        active_specialities_id = []
        for course in all_active_courses:
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

        course_q = BasicCourse.objects.filter(id=lesson_details['course_id'])
        lessons = course_q.first().lesson_set.all().order_by('order')

        lessons_details = []
        for i, lesson in enumerate(lessons):
            details = get_lesson_details(lesson.id, detail_contents=False)
            details['index'] = i + 1;
            if details['id'] == lesson_details['id']:
                lesson_details['index'] = i + 1;

            lessons_details.append(details)

        course_details = get_courses_details(course_q)[0]
        course_details['lessons'] = lessons_details;

        lesson_details['course'] = course_details;

        context['lesson'] = lesson_details

        print(lesson_details);

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