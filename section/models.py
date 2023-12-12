from django.db import models
from django.utils.timezone import now

from users.models import UserModel


class SectionModel(models.Model):
    name = models.CharField(max_length=155)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    trainers = models.ManyToManyField(to=UserModel)
    students = models.ManyToManyField(to=UserModel)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=now())


class GroupModel(models.Model):
    name = models.CharField(max_length=155)
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE)
    trainers = models.ManyToManyField(to=UserModel)
    students = models.ManyToManyField(to=UserModel)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=now())


class LessonModel(models.Model):
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField()
    is_canceled = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=now())
