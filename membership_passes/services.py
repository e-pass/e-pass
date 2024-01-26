import datetime
from typing import Any, Type


def _check_object_entry_in_db_by_id(model: Any, object_id: int) -> bool:
    """Функция проверки записи в БД"""
    return model.objects.filter(id=object_id).exists()

def _check_expiration_period(valid_from: datetime, valid_until: datetime) -> bool:
    """Функция проверки правильного ввода периода действия"""
    return valid_from <= valid_until

def _check_expiration_date(valid_until: datetime):
    """Функция проверки даты окончания периода действия абонемента"""
    if valid_until < datetime.date.today():
        return False
    return True

def _check_expiration_total(valid_from: datetime, valid_until: datetime) -> bool:
    """Функция полной проверки введённого периода действия и сравнения с текущей датой"""
    return all((_check_expiration_period(valid_from, valid_until), _check_expiration_date(valid_until)))

def _check_object_for_expiration_date(instance: Type['PassModel']) -> Type['PassModel']:
    """Функция установки поля is_active в False, если срок действия абонемента закончился"""
    if instance.is_active and not _check_expiration_date(instance.valid_until):
        instance.is_active = False
        instance.save()
    return instance
