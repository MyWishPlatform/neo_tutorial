from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=120, db_index=True)


class LessonContent(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    raw_text = models.TextField()


class CourseImage(models.Model):
    #course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE, default='')
    image = models.ImageField(upload_to='course_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CourseTag(models.Model):
    name = models.CharField(max_length=120, db_index=True)


class BasicCourse(models.Model):
    name = models.CharField(max_length=80, null=True, default='')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=120, null=True, default=None)
    image = models.ForeignKey(CourseImage, on_delete=models.CASCADE, default='', null=True)
    tag = models.ForeignKey(CourseTag, on_delete=models.CASCADE, default='')
    #def get_image(self):
    #    return CourseImage.objects.get(course=self)


class CourseMaterial(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default=None)
    media_url = models.CharField(max_length=120, null=True, default=None)
    raw_text = models.TextField()


class Lesson(models.Model):
    course = models.ForeignKey(BasicCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default=None)
    video_url = models.CharField(max_length=120, null=True, default=None)
    content = models.ForeignKey(LessonContent, on_delete=models.CASCADE)
    #test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, default='')
    description = models.CharField(max_length=120, null=True, default=None)
