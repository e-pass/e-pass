from django.contrib.auth.backends import UserModel
from django.db import models
from django.core import validators

from membership_passes.validation import check_expiration_date
from sections.models import SectionModel


class PassModel(models.Model):
    """Модель Абонемент"""
    name = models.CharField(max_length=100)
    student = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='my_passes')
    section = models.ForeignKey(to=SectionModel, on_delete=models.CASCADE, related_name='section_passes')
    quantity_lessons_max = models.PositiveIntegerField(validators=[validators.MinValueValidator(1)])
    is_unlimited = models.BooleanField(default=False)
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
            self.is_active = check_expiration_date(self.valid_until)
        super(PassModel, self).save(*args, **kwargs)


class EntryModel(models.Model):
    """Модель Отметка посещения"""
    to_pass = models.ForeignKey(to=PassModel, on_delete=models.CASCADE, related_name='entries')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)
