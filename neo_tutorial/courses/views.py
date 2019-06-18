from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError
from django.http import HttpResponseBadRequest
from .models import BasicCourse, LessonContent, CourseMaterial, Lesson, Test, Speciality, CourseImage
from .api import get_or_create_speciality, get_or_create_tag


@api_view(http_method_names=['GET'])
def all_courses_view(request):
    all_courses = BasicCourse.objects.all()

    details = []
    for c in all_courses:
        course_details = {
            'id': c.id,
            'name': c.name,
            'speciality': c.speciality.name,
            'description': c.description,
            'image': {}
        }
        if c.image is not None:
            saved_image = c.image

            course_details['image'] = {
                "id": saved_image.id,
                'image_url': saved_image.image.name,
                'uploaded_at': saved_image.uploaded_at
            }
        details.append(course_details)

    return Response(details)


@api_view(http_method_names=['POST'])
def create_course_view(request):

    params = request.data
    print(params)

    if 'name' not in params:
        raise ParseError('Name of course is required')

    if 'speciality' not in params:
        raise ParseError('Speciality of course is required')

    speciality = get_or_create_speciality(params['speciality'])
    if speciality is None:
        return HttpResponseBadRequest('Speciality with id {id} already exists'.format(id=params['speciality']))

    description = params['description'] if 'description' in params else ''

    tag = get_or_create_tag(params['tag'])
    if tag is None:
        return HttpResponseBadRequest('Tag with id {id} already exists'.format(id=params['tag']))


    course = BasicCourse(
            name=params['name'],
            speciality=speciality,
            description=description,
            tag=tag
    )

    image_details = {}
    if 'image' in params:
        saved_image = CourseImage(image=request.FILES['image'])
        saved_image.save()
        course.image = saved_image
        image_details = {
            "id": saved_image.id,
            'image_url': saved_image.image.name,
            'uploaded_at': saved_image.uploaded_at
        }

    course.save()

    details = {
        'id': course.id,
        'name': course.name,
        'speciality': course.speciality.name,
        'description': course.description,
        'tag': course.tag.name,
        'image': image_details
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
        return HttpResponseBadRequest('Course with id {course_id} is not found'.format(course_id=course_id))

    if 'speciality' in params:
        speciality = get_or_create_speciality(params['speciality'])
        if speciality is None:
            return HttpResponseBadRequest('Speciality with id {id} already exists'.format(id=params['speciality']))
        else:
            course.speciality = speciality

    if 'description' in params:
        course.description = params['description']

    if 'image_url' in params:
        course.image_url = params['image_url']

    course.save()

    updated_details = {
        'name': course.name,
        'speciality': course.speciality.name,
        'description': course.description,
        'image_url': course.image_url
    }

    return Response(updated_details)


