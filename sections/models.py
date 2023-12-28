from django.db import models
from django.utils.timezone import now

from users.models import StudentModel, TrainerModel


class SectionModel(models.Model):
    name = models.CharField(max_length=155)
    owner = models.ForeignKey(to=TrainerModel, on_delete=models.CASCADE, related_name='my_own_section')
    trainers = models.ManyToManyField(to=TrainerModel, related_name='section')
    students = models.ManyToManyField(to=StudentModel, related_name='section')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Name: {self.name} | Owner: {self.owner}'


class GroupModel(models.Model):
    name = models.CharField(max_length=155)
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='groups')
    trainers = models.ManyToManyField(to=TrainerModel, related_name='my_groups')
    students = models.ManyToManyField(to=StudentModel, related_name='my_groups')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Name: {self.name} | Section: {self.section.name}'


class LessonModel(models.Model):
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField()
    is_canceled = models.BooleanField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
