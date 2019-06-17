from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=120, db_index=True)


class LessonContent(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    raw_text = models.TextField()


class BasicCourse(models.Model):
    name = models.CharField(max_length=80, null=True, default='')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=120, null=True, default=None)
    image_url = models.CharField(max_length=120, null=True, default=None)


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
