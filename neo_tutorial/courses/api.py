from os.path import join
from rest_framework.exceptions import ParseError
from .models import BasicCourse, Speciality, CourseImage, LessonImage


def get_or_create_speciality(param, type):
    if type != "1":
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
        saved_image = c.courseimage_set.all().order_by('-uploaded_at').first()
        if saved_image:
            course_details['image'] = {
                'image_name': saved_image.image.name,
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


def parse_image_course(course_object, file):
    saved_image = CourseImage(course=course_object, image=file)
    saved_image.save()
    details = {
        'image_name': saved_image.image.name,
        'uploaded_at': saved_image.uploaded_at
    }
    return details


def parse_image_lesson(lesson_object, file):
    lesson_name = lesson_object.name
    saved_image = LessonImage(lesson=lesson_object, image=file)
    saved_image.image.upload_to=join("lesson_images", lesson_name)
    saved_image.save()
    details = {
        'lesson_name': lesson_name,
        'image_id': saved_image.id,
        'image_name': saved_image.image.name,
        'uploaded_at': saved_image.uploaded_at
    }
    return details
