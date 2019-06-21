from rest_framework.exceptions import ParseError
from .models import BasicCourse, Speciality, CourseImage, LessonImage, Lesson
from datetime import datetime


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
    time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    file.name = "{course_id}_image_{timestamp}".format(
            course_id=course_object.id,
            timestamp=time_now)
    saved_image = CourseImage(
            course=course_object,
            image=file,
            uploaded_at=time_now
    )
    saved_image.save()
    details = {
        'image_name': saved_image.image.name,
        'uploaded_at': saved_image.uploaded_at,
        'image_url': saved_image.image.url
    }
    return details


def parse_image_lesson(lesson_object, file):
    time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    file.name = "{lesson_id}_image_{timestamp}".format(
            lesson_id=lesson_object.id,
            timestamp=time_now)
    saved_image = LessonImage(
            lesson=lesson_object,
            image=file,
            uploaded_at=time_now
    )
    saved_image.save()
    details = {
        'lesson_name': lesson_object.name,
        'image_id': saved_image.id,
        'image_name': saved_image.image.name,
        'uploaded_at': saved_image.uploaded_at,
        'image_url': saved_image.image.url
    }
    return details


def get_lesson_details(lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ParseError('Lesson with id {id} not exists'.format(id=lesson_id))

    details = {
        'id': lesson.id,
        'course_id': lesson.course_id,
        'name': lesson.name,
        'description': lesson.description,
        'video_id': lesson.video_id,
        'content': lesson.content,
        'order': lesson.order
    }
    return details


def get_specialities():
    all_specialities = Speciality.objects.all()
    details = []
    for speciality in all_specialities:
        details.append({
            'id': speciality.id,
            'name': speciality.name
        })

    return details
