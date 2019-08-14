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
            'speciality': {
                'id': c.speciality.id,
                'name': c.speciality.name
            },
            'description': c.description,
            'image': {},
            'tags': c.tags,
            'is_active': c.is_active,
            'updated_at': c.updated_at,
            'course_id': c.course_id,
            'lng': c.lng,
            'other_lang_ids': get_langs_for_course(c.id)
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


def get_lesson_details(lesson_id, detail_contents=True):
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
#        'content': lesson.content,
        'order': lesson.order
    }

    if detail_contents:
        details['content'] = lesson.content
    return details


def get_speciality_by_id(speciality_id):
    speciality = Speciality.objects.get(id=speciality_id)
    details = {
        'id': speciality.id,
        'name': speciality.name
    }
    return details


def get_field_values(field, course_set):
    active_field_values = []
    for course in course_set:
        field_value = getattr(course, field)
        lessons_count = Lesson.objects.filter(id=course.id).order_by('-order')
        if field_value not in active_field_values and len(lessons_count) > 0:
            active_field_values.append(field_value)

    return active_field_values


def get_languages(course_set):
    active_language_names = []
    for course in course_set:
        lng_name = course.lng
        lessons_count = Lesson.objects.filter(id=course.id).order_by('-order')
        if lng_name not in active_language_names:
            if len(lessons_count) > 0:
                active_language_names.append(lng_name)

    return active_language_names


def get_specialities(course_set):
    active_specialities = []
    for course in course_set:
        spec_id = course.speciality_id
        lessons_count = Lesson.objects.filter(id=course.id).order_by('-order')
        if spec_id not in active_specialities:
            if len(lessons_count) > 0:
                active_specialities.append(spec_id)

    return active_specialities


def get_langs_for_course(course_id):
    other_lang_courses = BasicCourse.objects.filter(course_id=course_id, is_active=True).order_by('id')

    internal_ids = {}
    for course_other_lang in other_lang_courses:
        lessons_count = len(Lesson.objects.filter(course=course_other_lang).order_by('order'))
        if lessons_count > 0:
            internal_ids[course_other_lang.lng] = course_other_lang.id

    return internal_ids
