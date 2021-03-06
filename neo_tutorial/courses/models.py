from django.db import models
from django.contrib.postgres.fields import ArrayField

from neo_tutorial.profile.models import TutorialUser


class Speciality(models.Model):
    name = models.CharField(max_length=120, db_index=True, unique=True)
#    image = models.ImageField(upload_to='speciality_images')


#class LessonContent(models.Model):
#    name = models.CharField(max_length=120, db_index=True)
#    raw_text = models.TextField()


class BasicCourse(models.Model):
    name = models.CharField(max_length=80, null=True, default='')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=120, null=True, default='')
    course_id = models.IntegerField()
    lng = models.CharField(max_length=80, default='en')

    tags = ArrayField(
            base_field=models.CharField(max_length=30, null=True, default=''),
            null=True
    )
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image(self):
        image= self.courseimage_set.all().order_by('-uploaded_at').first()
        return image

    def get_image_details(self):
        saved_image = self.get_image()
        if saved_image:
            details = {
                'image_name': saved_image.image.name,
                'uploaded_at': saved_image.uploaded_at
            }
        else:
            details = {}
        return details


class CourseImage(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE, default='')
    image = models.ImageField(upload_to='course_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default='')
    video_id = models.CharField(max_length=120, null=True, default='')
    content = models.TextField()
    order = models.IntegerField(null=True, default=None)


class LessonImage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default='')
    image = models.ImageField(upload_to='lesson_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CourseMaterial(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default=None)
    media_url = models.CharField(max_length=120, null=True, default=None)
    raw_text = models.TextField()


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default=None)


class CompletedCourses(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE)
    user = models.ForeignKey(TutorialUser, on_delete=models.CASCADE)


class CompletedLessons(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(TutorialUser, on_delete=models.CASCADE)
