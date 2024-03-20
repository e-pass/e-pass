import datetime
from collections import namedtuple
from typing import Any, Optional, Type

from django.conf import settings
from django.http import Http404
from django.utils import timezone
from rest_framework import serializers

from sections.models import SectionModel


def check_object_entry_in_db_by_id(model: Any, object_id: int) -> bool:
    """Функция проверки наличия записи в БД"""
    return model.objects.filter(id=object_id).exists()


def get_section_object_from_db(section_id: int, need_return=False) -> Type['SectionModel'] | None:
    """Функция проверки наличия записи в БД. Возврат объекта по запросу."""
    try:
        section = SectionModel.objects.get(id=section_id)
        return section if need_return else None
    except SectionModel.DoesNotExist:
        raise Http404(f'Секции с id {section_id} не существует. Проверьте параметры запроса')


def get_pass_object_from_db(pass_id: int) -> Optional['PassModel']:
    """Функция проверки наличия записи в БД."""
    from membership_passes.models import PassModel

    try:
        pass_obj = PassModel.objects.get(id=pass_id)
        return pass_obj
    except PassModel.DoesNotExist:
        raise serializers.ValidationError(
            detail=f'Абонемента с id {pass_id} не существует. Проверьте параметры запроса'
        )


def check_expiration_period(valid_from: datetime, valid_until: datetime) -> bool:
    """Функция проверки правильного ввода периода действия"""
    return valid_from <= valid_until


def check_expiration_date(valid_until: datetime) -> bool:
    """Функция проверки даты окончания периода действия абонемента"""
    if valid_until < datetime.date.today():
        return False
    return True


def check_max_expiration_date(valid_until: datetime) -> None:
    """Функция проверки максимального аериода действия"""
    if valid_until > datetime.date(2100, 1, 1):
        raise serializers.ValidationError(
            detail='Максимальный срок действия до 01 января 2100')


def check_expiration_total(valid_from: datetime, valid_until: datetime) -> None:
    """Функция полной проверки введённого периода действия и сравнения с текущей датой"""
    check_max_expiration_date(valid_until)
    if not all((check_expiration_period(valid_from, valid_until), check_expiration_date(valid_until))):
        raise serializers.ValidationError(detail='Введён некорректный период действия.')


def check_periods_crossing(exist_range: namedtuple, new_range: namedtuple) -> Optional[int]:
    """Функция подсчёта количества общих дней в двух временных периодах"""
    latest_start = max(exist_range.start, new_range.start)
    earliest_end = min(exist_range.end, new_range.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(delta, 0)
    return overlap if overlap > 0 else None


def check_existing_passes(validated_data: dict) -> None:
    """Функция проверки уже существующих активных абонементов пользователя
    на предмет пересечения сроков действия с новым абонементом"""
    from membership_passes.models import PassModel

    section_id = validated_data['section'].id
    student_id = validated_data['student'].id
    valid_until = validated_data['valid_until']
    valid_from = validated_data['valid_from']
    self_id = validated_data.get('pass_id', None)

    Range = namedtuple('Range', field_names=['start', 'end'])

    new_range = Range(start=valid_from, end=valid_until)

    student_passes = PassModel.objects.filter(
        student_id=student_id,
        section_id=section_id,
        is_active=True
    ).exclude(id=self_id).only('valid_from', 'valid_until')

    for st_pass in student_passes:
        exist_range = Range(start=st_pass.valid_from, end=st_pass.valid_until)
        if check_periods_crossing(exist_range, new_range):
            raise serializers.ValidationError(
                detail='На эти даты уже имеется абонемент для данного пользователя.')


def check_last_entry(last_entry_time: datetime) -> None:
    """Функция проверки времени предыдущего сканирования"""
    now = timezone.now()

    if last_entry_time + settings.CHECK_IN_FREQUENCY > now:
        timediff = (last_entry_time + settings.CHECK_IN_FREQUENCY - now)
        raise serializers.ValidationError(
            detail=f'Ошибка! Следующее сканирование не раньше, чем через {str(timediff).split(".")[0]}')


def check_unused_lessons_quantity(pass_obj: Type['PassModel'], quantity_entries: int) -> None:
    """Функция проверки количества неиспользованных занятий"""
    if pass_obj.quantity_lessons_max - quantity_entries <= 0:
        raise serializers.ValidationError(detail='У абонемента закончилось кол-во занятий.')


def check_pass_activity(pass_obj: Type['PassModel']) -> None:
    """Функция проверки поля is_active у абонемента"""
    if not pass_obj.is_active:
        raise serializers.ValidationError(detail='Абонемент неактивен.')


def check_pass_is_paid(pass_obj: Type['PassModel']) -> None:
    if not pass_obj.is_paid:
        raise serializers.ValidationError(detail='Абонемент не оплачен.')


def check_pass_valid_from(pass_obj: Type['PassModel']) -> None:
    if datetime.date.today() < pass_obj.valid_from:
        raise serializers.ValidationError(
            detail=f'Ошибка. Абонемент будет действителен для сканирования с {pass_obj.valid_from}')


def check_pass_before_check_in(pass_id: int) -> Type['PassModel']:
    """Функция получения абонемента из БД и проверки возможности сканирования"""
    from membership_passes.models import EntryModel
    pass_obj = get_pass_object_from_db(pass_id=pass_id)
    entries = EntryModel.objects.filter(to_pass=pass_id).order_by('created_at')
    quantity_entries = entries.count()

    check_pass_activity(pass_obj=pass_obj)
    check_pass_is_paid(pass_obj=pass_obj)
    check_pass_valid_from(pass_obj=pass_obj)
    if quantity_entries > 0:
        check_unused_lessons_quantity(pass_obj=pass_obj, quantity_entries=quantity_entries)
        check_last_entry(last_entry_time=entries.last().created_at)

    return pass_obj
