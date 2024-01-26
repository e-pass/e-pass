from membership_passes.services import _check_expiration_date

from django.contrib.auth.backends import UserModel
from django.db import models

from sections.models import SectionModel, LessonModel
from django.core import validators


class PassModel(models.Model):
    """Модель абонемент"""
    name = models.CharField(max_length=100)
    student = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='my_passes')
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='section_passes')
    qr_code = models.CharField(max_length=255, validators=[validators.URLValidator], unique=True)
    quantity_lessons_max = models.PositiveIntegerField(default=0)
    quantity_unused_lessons = models.IntegerField(default=0, editable=False)
    lessons = models.ManyToManyField(to=LessonModel, blank=True, related_name='used_passes')
    is_unlimited = models.BooleanField()
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}. {self.student.first_name} {self.student.last_name}. Valid until{self.valid_until}'

    def save(self, *args, **kwargs):
        """При создании нового абонемента устанавливается количество
        неиспользованных уроков равное максимальному.
        При каждом сохранении в базу данных проверяется срок действия,
        при необходимости поле is_active меняется на False"""
        creating = not self.pk
        if creating:
            self.quantity_unused_lessons = self.quantity_lessons_max

        if self.is_active:
            self.is_active = _check_expiration_date(self.valid_until)
        super(PassModel, self).save(*args, **kwargs)

