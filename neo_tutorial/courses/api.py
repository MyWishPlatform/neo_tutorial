from .models import BasicCourse, LessonContent, CourseMaterial, Lesson, Test, Speciality
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Speciality, CourseTag
from django.http import HttpResponseBadRequest


def get_or_create_object(course_object, param):
    if isinstance(param, int):
        try:
            obj = course_object.objects.get(id=param)
            return obj
        except course_object.DoesNotExist:
            return None
    else:
        new_obj = course_object(name=param)
        new_obj.save()
        return new_obj


def get_or_create_speciality(param):
    return get_or_create_object(Speciality, param)


def get_or_create_tag(param):
    return get_or_create_object(CourseTag, param)
