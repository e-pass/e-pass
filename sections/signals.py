from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from sections.models import LessonModel


@receiver(m2m_changed, sender=LessonModel.group.students.through)
def update_group_type(sender, instance, action) -> None:
    if action == 'post_add' or action == 'post_remove':
        if instance.students.count() == 1:
            instance.type = LessonModel.INDIVIDUAL
        else:
            instance.type = LessonModel.GROUP
        instance.save()
