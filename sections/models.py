from django.db import models
from django.utils.timezone import now

from users.models import UserModel


class SectionModel(models.Model):
    name = models.CharField(max_length=155)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='my_own_section')
    trainers = models.ManyToManyField(to=UserModel, related_name='trainer_section')
    students = models.ManyToManyField(to=UserModel, related_name='student_section')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GroupModel(models.Model):
    name = models.CharField(max_length=155)
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='groups')
    trainers = models.ManyToManyField(to=UserModel, related_name='trainer_groups')
    students = models.ManyToManyField(to=UserModel, related_name='student_groups')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LessonModel(models.Model):
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField()
    is_canceled = models.BooleanField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
