from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from neo_tutorial.courses.api import get_all_courses_details, get_lesson_details, get_speciality_by_id, \
    get_courses_details, get_languages, get_specialities
from neo_tutorial.courses.models import BasicCourse, Lesson, CompletedCourses, CompletedLessons


def require_login():
    return HttpResponseRedirect('/login')


class HomeView(TemplateView):
    template_name = 'portal/home.html'


class HomeLoginView(HomeView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')


class HomePasswordChangeView(HomeView):
    pass
    #def get(self, request, *args, **kwargs):
    #    return HttpResponseRedirect('/')


class CourseListView(TemplateView):
    template_name = 'portal/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_courses = BasicCourse.objects.filter(is_active=True).order_by('id')
        all_active_courses = active_courses

        active_specialities_id = []
        for course in all_active_courses:
            speciality_id = course.speciality_id
            if speciality_id not in active_specialities_id:
                active_specialities_id.append(course.speciality_id)

        active_specialities = []
        for spec_id in active_specialities_id:
            active_specialities.append(get_speciality_by_id(spec_id))
        context['speciality_list'] = active_specialities
        context['language_list'] = get_languages(all_active_courses)
        #print(context['speciality_list'])

        filter_tag = self.request.GET.get('q')
        filter_spec = self.request.GET.get('spec')
        filter_lng = self.request.GET.get('l')
        default_filter_lng = 'en'

        if filter_tag is not None:
            active_courses = active_courses.filter(tags__contains=[filter_tag])
            context['selected_tag'] = filter_tag

        if filter_spec is not None:
            active_courses = active_courses.filter(speciality_id=filter_spec)
            context['selected_spec'] = int(filter_spec)
            print('selected_spec', context['selected_spec'])
            if filter_lng is None:
                active_courses = active_courses.filter(lng=default_filter_lng)
                context['language_list'] = get_languages(all_active_courses)
                print('language_list', context['language_list'])
            else:
                context['language_list'] = get_languages(active_courses)
                print('language_list', context['language_list'])

        if filter_lng is not None:
            active_courses = active_courses.filter(lng=filter_lng)
            context['selected_lng'] = filter_lng
            if filter_spec is None:
                filtered_specs = []
                lng_specs = get_specialities(active_courses)
                for spec_id in lng_specs:
                    filtered_specs.append(get_speciality_by_id(spec_id))
                context['speciality_list'] = filtered_specs
                print('speciality_list', context['speciality_list'])
        else:
            context['selected_lng'] = default_filter_lng
            context['speciality_list'] = active_specialities

        #print('spec_list_1', context['speciality_list'])
        #print('selected_lng', context['selected_lng'])

        if filter_lng is None and filter_spec is None:
            active_courses = active_courses.filter(lng='en')

        course_list = get_courses_details(active_courses)
        context['courses'] = course_list
        print(context['courses'])

        return context


class CourseLessonView(TemplateView):
    template_name = 'portal/course_lesson.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return require_login()

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_details = get_lesson_details(id)
        this_lesson = Lesson.objects.get(id=id)

        course_q = BasicCourse.objects.filter(id=lesson_details['course_id'])
        this_course = course_q.first()
        lessons = this_course.lesson_set.all().order_by('order')

        lessons_details = []
        for i, lesson in enumerate(lessons):
            details = get_lesson_details(lesson.id, detail_contents=False)
            details['index'] = i + 1
            if details['id'] == lesson_details['id']:
                lesson_details['index'] = i + 1

            lessons_details.append(details)

        course_details = get_courses_details(course_q)[0]

        course_details['lessons'] = lessons_details
        lesson_details['course'] = course_details
        context['lesson'] = lesson_details

        current_user = self.request.user

        main_course = BasicCourse.objects.get(id=this_course.course_id)
        #main_lesson = Lesson.objects.get(id=this_lesson.course_id)
        main_lng_lesson = Lesson.objects.get(order=this_lesson.order, course=main_course)
        print(main_course)
        print(main_lng_lesson)

        lesson_completed, created_now_l = CompletedLessons.objects.get_or_create(
                course=main_course,
                lesson=main_lng_lesson,
                user=current_user
        )
        if created_now_l:
            lesson_completed.save()

        completed_in_course = CompletedLessons.objects.filter(
                course=main_course,
                user=current_user
        )
        if len(completed_in_course) == len(lessons):
            course_completed, created_now_q = CompletedCourses.objects.get_or_create(
                    course=main_course,
                    user=current_user
            )
            if created_now_q:
                course_completed.save()

        return context


class CourseView(TemplateView):
    template_name = 'portal/course.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return require_login()

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        course_q = BasicCourse.objects.filter(id=id)
        course_details = get_courses_details(course_q)[0]

        context['course'] = course_details
        print(context['course'])

        lessons = course_q.first().lesson_set.all().order_by('order')

        lessons_details = []
        for lesson in lessons:
            details = get_lesson_details(lesson.id, detail_contents=False)
            lessons_details.append(details)

        context['lessons'] = lessons_details


        return context