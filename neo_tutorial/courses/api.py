from .models import BasicCourse, LessonContent, CourseMaterial, Lesson, Test, Speciality
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import BasicCourse, Speciality
from django.http import HttpResponseBadRequest


def get_or_create_speciality(param):
    if isinstance(param, int):
        try:
            obj = Speciality.objects.get(id=param)
            return obj
        except Speciality.DoesNotExist:
            raise ParseError('Speciality with id {id} not exists'.format(id=param))
    else:
        try:
            speciality = Speciality.objects.get(name=param)
            raise ParseError('Speciality with name {name} already exists'.format(name=param))
        except Speciality.DoesNotExist:
            new_obj = Speciality(name=param)
            new_obj.save()
            return new_obj


def get_courses_details(courses_queryset):
    details = []
    for c in courses_queryset:
        course_details = {
            'id': c.id,
            'name': c.name,
            'speciality': c.speciality.name,
            'description': c.description,
            'image': {},
            'tags': c.tags
        }
        if c.image is not None:
            saved_image = c.image

            course_details['image'] = {
                "id": saved_image.id,
                'image_url': saved_image.image.name,
                'uploaded_at': saved_image.uploaded_at
            }
        details.append(course_details)
    return details


def get_all_courses_details():
    all_courses = BasicCourse.objects.all()
    details = get_courses_details(all_courses)
    return details


def get_courses_by_tag(tag_param):
    courses = BasicCourse.objects.filter(tags__contains=[tag_param])
    return courses


def get_courses_by_tag_details(tag_param):
    courses = get_courses_by_tag(tag_param)
    details = get_courses_details(courses)
    return details

