from django.db import models
from django.utils.timezone import now

from users.models import UserModel


class SectionModel(models.Model):
    name = models.CharField(max_length=155)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    trainers = models.ManyToManyField(to=UserModel, related_name='section_trainers')
    students = models.ManyToManyField(to=UserModel, related_name='students_trainers')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)


class GroupModel(models.Model):
    name = models.CharField(max_length=155)
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE)
    trainers = models.ManyToManyField(to=UserModel, related_name='group_trainers')
    students = models.ManyToManyField(to=UserModel, related_name='group_students')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)


class LessonModel(models.Model):
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField()
    is_canceled = models.BooleanField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
