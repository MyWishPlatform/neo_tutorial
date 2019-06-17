from django.db import models


class BasicCourse(models.Model):
    name = models.CharField(max_length=80, null=True, default='')
