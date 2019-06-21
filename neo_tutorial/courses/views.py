from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError
from .models import BasicCourse, CourseMaterial, Lesson, Test, Speciality, CourseImage
from .api import get_courses_details, get_or_create_speciality, get_all_courses_details, get_courses_by_tag_details, \
    parse_image_course, parse_image_lesson, get_lesson_details
from ast import literal_eval


@api_view(http_method_names=['GET'])
def all_courses_view(request):
    return Response(get_all_courses_details())


@api_view(http_method_names=['POST'])
def create_course_view(request):

    params = request.data

    if 'name' not in params:
        raise ParseError('Name of course is required')

    if 'speciality' not in params:
        raise ParseError('Speciality of course is required')

    if 'new_speciality' not in params:
        new_speciality = ""
    else:
        new_speciality = params['new_speciality']

    speciality = get_or_create_speciality(params['speciality'], new_speciality)
    description = params['description'] if 'description' in params else ''

    if 'tags' not in params:
        tag_list = []
    else:
        tag_list_representation = params['tags']
        tag_list = literal_eval(tag_list_representation)

    course = BasicCourse(
            name=params['name'],
            speciality=speciality,
            description=description,
            tags=tag_list
    )
    course.save()

    image_details = {}
    if 'image' in params:
        image_details = parse_image_course(course, request.FILES['image'])

    details = {
        'id': course.id,
        'name': course.name,
        'speciality': course.speciality.name,
        'description': course.description,
        'tags': course.tags,
        'image': image_details,
        'is_active': False,
        'updated_at': course.updated_at
    }
    return Response(details)


@api_view(http_method_names=['POST'])
def update_course_view(request):
    params = request.data
    if 'id' not in params:
        raise ParseError('id of course is required')
    else:
        course_id = params['id']

    try:
        course = BasicCourse.objects.get(id=course_id)
    except BasicCourse.DoesNotExist:
        raise ParseError('Course with id {course_id} is not found'.format(course_id=course_id))

    if 'speciality' in params:
        if 'new_speciality' not in params:
            new_speciality = ""
        else:
            new_speciality = params['new_speciality']

        course.speciality = get_or_create_speciality(params['speciality'], new_speciality)

    if 'description' in params:
        course.description = params['description']

    if 'name' in params:
        course.name = params['name']

    if 'tags' in params:
        tag_list_representation = params['tags']
        tag_list = literal_eval(tag_list_representation)
        course.tags = tag_list

    image_details = course.get_image_details()

    if 'image' in params:
        image_details = parse_image_course(course, request.FILES['image'])

    if 'is_active' in params:
        course.is_active = params['is_active']

    course.save()

    updated_details = {
        'id': course.id,
        'name': course.name,
        'speciality': course.speciality.name,
        'description': course.description,
        'tags': course.tags,
        'image': image_details,
        'is_active': course.is_active,
        'updated_at': course.updated_at
    }

    return Response(updated_details)


@api_view(http_method_names=['GET'])
def get_course_view(request, id):

    if not id:
        raise ParseError('id of course is required')

    course = BasicCourse.objects.filter(id=id)
    details = get_courses_details(course)[0]
    return Response(details)


@api_view(http_method_names=['GET'])
def get_courses_by_tag_view(request):
    if 'tag' not in request.data:
        raise ParseError('Tag not specified')

    details = get_courses_by_tag_details(request.data['tag'])
    return Response(details)


@api_view(http_method_names=['GET'])
def get_specialities_view(request):
    speciality_list = Speciality.objects.all()

    speciality_details = []
    for speciality in speciality_list:
        speciality_details.append({
            'id': speciality.id,
            'name': speciality.name
        })
    return Response(speciality_details)


@api_view(http_method_names=['GET'])
def get_lessons_by_course_view(request, course_id):
    if not course_id:
        raise ParseError('id of course is required')

    course = BasicCourse.objects.filter(id=course_id).first()
    lessons = course.lesson_set.all().order_by('id')

    lessons_details = []
    for lesson in lessons:
        details = get_lesson_details(lesson.id)

        if lesson.lessonimage_set.all():
            images = lesson.lessonimage_set.all()
            images_details = []
            for lesson_image in images:
                images_details.append({
                    'name': lesson_image.image.name,
                    'uploaded_at': lesson_image.uploaded_at
                })
            details['images'] = images_details

        lessons_details.append(details)
    return Response(lessons_details)


@api_view(http_method_names=['POST'])
def create_lesson_view(request):
    params = request.data

    if 'name' not in params:
        raise ParseError('Name of lesson is required')

    if 'course_id' not in params:
        course_object = None
        course_name = ""
    else:
        course_object = BasicCourse.objects.filter(id=params['course_id']).first()
        course_name = course_object.name

    description = params['description'] if 'description' in params else ""
    video_id = params['video_id'] if 'video_id' in params else ""
    content = params['content'] if 'content' in params else ""
    order = params['order'] if 'order' in params else ""

    lesson = Lesson(
            course=course_object,
            name=params['name'],
            description=description,
            video_id=video_id,
            content=content,
            order=order
    )
    lesson.save()

    details = {
        'id': lesson.id,
        'course_name': course_name,
        'name': lesson.name,
        'description': lesson.description,
        'video_id': lesson.video_id,
        'content': lesson.content,
        'order': lesson.order
    }
    return Response(details)


@api_view(http_method_names=['POST'])
def upload_lesson_images_view(request):
    if 'lesson_id' not in request.data:
        raise ParseError('id of lesson is required')

    lesson_id = request.data['lesson_id']
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ParseError('Lesson with id {lesson_id} is not found'.format(lesson_id=lesson_id))

    if not request.FILES:
        raise ParseError('no images for upload')

    content_images = request.FILES

    images_details = []
    for image in content_images:
        saved_images = parse_image_lesson(lesson, content_images[image])
        images_details.append(saved_images)

    return Response(images_details)


@api_view(http_method_names=['POST'])
def edit_lesson_view(request):
    if 'id' not in request.data:
        raise ParseError('id of lesson is required')

    params = request.data
    lesson_id = params['id']
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ParseError('Lesson with id {lesson_id} is not found'.format(lesson_id=lesson_id))

    if 'content' not in request.data:
        raise ParseError('content must be passed for edit')

    description = params['description'] if 'description' in params else lesson.description
    video_id = params['video_id'] if 'video_id' in params else lesson.video_id
    new_content = request.data['content']
    lesson_order = params['order'] if 'order' in params else lesson.order

    lesson.description = description
    lesson.video_id = video_id
    lesson.content = new_content
    lesson.order = lesson_order

    lesson.save()

    details = {
        'id': lesson.id,
        'course_id': lesson.course.id,
        'name': lesson.name,
        'description': lesson.description,
        'video_id': lesson.video_id,
        'content': lesson.content,
        'order': lesson.order
    }

    return Response(details)


@api_view(http_method_names=['GET'])
def preview_lesson_view(request, id):
    if not id:
        raise ParseError('id of lesson is required')

    lesson_details = get_lesson_details(id)
    return Response(lesson_details)


@api_view(http_method_names=['POST', 'DELETE'])
def delete_lesson_view(request):
    if 'lesson_id' not in request.data:
        raise ParseError('id of lesson is required')

    lesson_id = request.data['lesson_id']
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ParseError('Lesson with id {lesson_id} is not found'.format(lesson_id=lesson_id))
    lesson.delete()
    return Response({"detail": "lesson {name} with id {id} deleted".format(
            name=lesson.name, id=lesson.id
    )})
