from django.db import models
from django.utils.timezone import now

from sections.utils.enums import LessonTypeEnum
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
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE)
    lesson_datetime = models.DateTimeField()
    duration = models.FloatField(default=50)
    is_canceled = models.BooleanField(default=False)
    type = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ) -> None:
        students_count = self.group.students.count()
        if students_count == 1:
            self.type = LessonTypeEnum.INDIVIDUAL.value
        else:
            self.type = LessonTypeEnum.GROUP.value
        return super().save()
