import datetime

from celery import shared_task

from membership_passes.models import PassModel


@shared_task
def check_passes() -> None:
    today = datetime.date.today()
    passes = PassModel.objects.filter(is_active=True, valid_until__lt=today
                                      ).prefetch_related('student')
    for p in passes:
        p.is_active = False
        p.save()
