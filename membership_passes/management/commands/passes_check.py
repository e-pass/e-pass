from datetime import datetime
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from membership_passes.models import PassModel


class Command(BaseCommand):
    """Команда для проверки окончания сроков действия абонементов и их деактивации при необходимости.
    Запускается при помощи check_script.py по расписанию"""
    help = 'Check the pass valid_until field'

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            passes = PassModel.objects.filter(is_active=True, valid_until__lt=(datetime.now())
                        ).prefetch_related('student')
            for p in passes:
                p.is_active = False
                p.save()

        except Exception as ex:
            raise CommandError('Something wrong!', ex)

        self.stdout.write(msg='Success!')