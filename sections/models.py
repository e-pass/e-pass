from django.db import models
from django.utils.timezone import now

from users.models import UserModel


class SectionModel(models.Model):
    title = models.CharField(max_length=155)
    owner = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='section_owner')
    trainers = models.ManyToManyField(to=UserModel, related_name='section_trainer')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Name: {self.title} | Owner: {self.owner}'


class GroupModel(models.Model):
    title = models.CharField(max_length=155)
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='groups')
    trainers = models.ManyToManyField(to=UserModel, related_name='trainers_groups')
    students = models.ManyToManyField(to=UserModel, related_name='student_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Name: {self.title} | Section: {self.section.title}'


class LessonModel(models.Model):
    INDIVIDUAL = 'individual'
    GROUP = 'group'

    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField()
    is_canceled = models.BooleanField()
    type = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
