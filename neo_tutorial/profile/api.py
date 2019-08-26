from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.urls import reverse
from os.path import join

from neo_tutorial.settings_local import HOST_URL
from neo_tutorial.courses.api import get_courses_details, get_lesson_details


class EmailConfirmTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


user_signup_token = EmailConfirmTokenGenerator()


def get_email_confirmation_url(request, uid, token):

    url = reverse('registration_email_confirm', args=[uid, token])

    response_url = '{scheme}://{host}{api_url}'.format(scheme=request.scheme, host=HOST_URL, api_url=url)
    return response_url


def get_password_change_url(request, uid, token):

    url = reverse('user_password_reset_confirm', args=[uid, token])
    response_url = '{scheme}://{host}{api_url}'.format(scheme=request.scheme, host=HOST_URL, api_url=url)
    return response_url


def get_user_completed_courses(user):
    courses = [x.course for x in user.completedcourses_set.all()]
    details = get_courses_details(courses)
    return details


def get_user_completed_lessons(user):
    lessons = [x.lesson for x in user.completedlessons_set.all()]
    details = []
    for lesson in lessons:
        details.append(get_lesson_details(lesson.id, detail_contents=False))
    return details


def get_full_user_statistics(user):
    courses = get_user_completed_courses(user)
    lessons = get_user_completed_lessons(user)
    res = {
        'completed_courses': courses,
        'completed_lessons': lessons,
        'completed_courses_count': len(courses),
        'completed_lessons_count': len(lessons)
    }

    return res
