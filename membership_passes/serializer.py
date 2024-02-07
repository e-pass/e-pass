from typing import OrderedDict
from django.conf import settings

from django.contrib.auth.backends import UserModel
from rest_framework import serializers, validators

from membership_passes.models import PassModel, EntryModel
from users.serializer import ShortUserSerializer

from membership_passes.validation import (check_expiration_total,
                                          check_existing_passes,
                                          check_pass_before_check_in)


class EntrySerializer(serializers.ModelSerializer):
    to_pass_id = serializers.IntegerField()
    class Meta:
        model = EntryModel
        fields = ('to_pass_id',)

    def validate(self, attrs):
        pass_obj = check_pass_before_check_in(attrs['to_pass_id'])
        attrs['to_pass'] = pass_obj
        return attrs




class PassSerializer(serializers.ModelSerializer):
    student = ShortUserSerializer(read_only=True)
    quantity_unused_lessons = serializers.IntegerField(read_only=True)
    valid_from = serializers.DateField(format=settings.REST_FRAMEWORK.get('DATE_INPUT_FORMATS')[0])
    valid_until = serializers.DateField(format=settings.REST_FRAMEWORK.get('DATE_INPUT_FORMATS')[0])

    class Meta:
        model = PassModel
        fields = ('id', 'name', 'student', 'section_id', 'qr_code', 'is_unlimited',
                  'quantity_lessons_max', 'quantity_unused_lessons', 'entries',
                  'is_active', 'valid_from', 'valid_until', 'price', 'is_paid')

    def to_representation(self, instance: PassModel) -> OrderedDict:
        ret = super(PassSerializer, self).to_representation(instance)
        if instance.is_unlimited:
            ret.pop("quantity_lessons_max")
            ret.pop("quantity_unused_lessons")
        else:
            ret.pop("is_unlimited")
        return ret


class CreatePassSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        source='student',
        queryset=UserModel.students.all().only('id'),
        write_only=True,
        error_messages={
            'does_not_exist': 'Введён некорректный id студента.'
        }
    )
    qr_code = serializers.URLField(validators=[validators.UniqueValidator(
        queryset=PassModel.objects.all().only('qr_code'),
        message="Ссылка на qr-код должна быть уникальной")])
    quantity_lessons_max = serializers.IntegerField(default=0)
    is_unlimited = serializers.BooleanField(default=False)
    valid_from = serializers.DateField(input_formats=settings.REST_FRAMEWORK.get('DATE_INPUT_FORMATS'))
    valid_until = serializers.DateField(input_formats=settings.REST_FRAMEWORK.get('DATE_INPUT_FORMATS'))
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    is_paid = serializers.BooleanField()

    class Meta:
        model = PassModel
        fields = ('name', 'student_id', 'is_unlimited', 'qr_code',
                  'quantity_lessons_max',
                  'valid_from', 'valid_until', 'price', 'is_paid')

    def validate(self, attrs):
        print(f'attrs: {attrs}')
        if self.context.get("request").method == 'POST':
            check_expiration_total(valid_from=attrs['valid_from'], valid_until=attrs['valid_until'])
            if attrs['quantity_lessons_max'] == 0 and attrs['is_unlimited'] is False:
                raise serializers.ValidationError("Установите максимальное количество уроков,"
                                                  " или активируйте поле 'Безлимитный'")
        return attrs

    def create(self, validated_data):
        check_existing_passes(validated_data)
        return super(CreatePassSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        student = validated_data.get('student', instance.student)
        section = validated_data.get('section', instance.section)
        valid_from = validated_data.get('valid_from', instance.valid_from)
        valid_until = validated_data.get('valid_until', instance.valid_until)
        pass_id = instance.id

        check_expiration_total(valid_from, valid_until)
        check_existing_passes({
            'student': student,
            'section': section,
            'valid_from': valid_from,
            'valid_until': valid_until,
            'pass_id': pass_id
        })

        return super(CreatePassSerializer, self).update(instance, validated_data)
