from django.contrib.auth.backends import UserModel
from django.db import models

from sections.models import SectionModel, GroupModel, LessonModel
from django.core import validators


class PassModel(models.Model):
    student = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='my_passes')
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='section_passes')
    group = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE, related_name='group_passes')
    qr_code = models.CharField(max_length=255, validators=[validators.URLValidator], unique=True)
    quantity_lessons_max = models.PositiveIntegerField(default=0)
    lessons = models.ManyToManyField(to=LessonModel, blank=True, related_name='used_passes')
    is_unlimited = models.BooleanField()
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} {self.section.name}'

