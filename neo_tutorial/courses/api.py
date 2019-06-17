from .models import BasicCourse, LessonContent, CourseMaterial, Lesson, Test, Speciality
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Speciality
from django.http import HttpResponseBadRequest


def get_or_create_speciality(param):
    if isinstance(param, int):
        try:
            speciality = Speciality.objects.get(id=param)
            return speciality
        except Speciality.DoesNotExist:
            return None
    else:
        new_speciality = Speciality(name=param)
        new_speciality.save()
        return new_speciality
