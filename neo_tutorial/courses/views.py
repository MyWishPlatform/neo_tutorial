from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError
from .models import BasicCourse, LessonContent, CourseMaterial, Lesson, Test, Speciality, CourseImage
from .api import get_courses_details, get_or_create_speciality, get_all_courses_details, get_courses_by_tag_details


@api_view(http_method_names=['GET'])
def all_courses_view(request):
    return Response(get_all_courses_details())


@api_view(http_method_names=['POST'])
def create_course_view(request):

    params = request.data
    print(params)

    if 'name' not in params:
        raise ParseError('Name of course is required')

    if 'speciality' not in params:
        raise ParseError('Speciality of course is required')

    speciality = get_or_create_speciality(params['speciality'])
    #if speciality is None:
    #    raise ParseError('Speciality with id {id} not exists'.format(id=params['speciality']))


    description = params['description'] if 'description' in params else ''
    tag_list = params['tags'] if 'tags' in params else []
    for x in tag_list:
        print(x)
    print(tag_list)
    print(tag_list.__class__)
    if not isinstance(tag_list, list):
        raise ParseError('Tags must be passed as list')

    course = BasicCourse(
            name=params['name'],
            speciality=speciality,
            description=description,
            tags=tag_list
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
        'tags': course.tags,
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
        raise ParseError('Course with id {course_id} is not found'.format(course_id=course_id))

    if 'speciality' in params:
        speciality = get_or_create_speciality(params['speciality'])
        if speciality is None:
            raise ParseError('Speciality with id {id} already exists'.format(id=params['speciality']))
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


@api_view(http_method_names=['GET'])
def get_course_view(request):
    if 'id' not in request.data:
        raise ParseError('id of course is required')

    course = BasicCourse.objects.filter(id=request.data['id'])
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
