import datetime
from typing import OrderedDict

from django.contrib.auth.backends import UserModel
from rest_framework import serializers, validators

from membership_passes.models import PassModel
from users.serializer import ShortUserSerializer


class PassSerializer(serializers.ModelSerializer):
    student = ShortUserSerializer(read_only=True)

    class Meta:
        model = PassModel
        fields = ('id', 'name', 'student', 'section_id', 'qr_code', 'is_unlimited',
                  'quantity_lessons_max', 'quantity_unused_lessons', 'lessons',
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
        write_only=True
    )
    qr_code = serializers.URLField(validators=[validators.UniqueValidator(
        queryset=PassModel.objects.all().only('qr_code'),
        message="Ссылка на qr-код должна быть уникальной")])
    quantity_lessons_max = serializers.IntegerField(default=0)
    is_unlimited = serializers.BooleanField(default=False)
    valid_from = serializers.DateField()
    valid_until = serializers.DateField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    is_paid = serializers.BooleanField()

    class Meta:
        model = PassModel
        fields = ('name', 'student_id', 'is_unlimited', 'qr_code',
                  'quantity_lessons_max', 'quantity_unused_lessons',
                  'valid_from', 'valid_until', 'price', 'is_paid')

    def validate(self, attrs):
        if attrs['valid_until'] < attrs['valid_from'] or attrs['valid_until'] < datetime.date.today():
            raise serializers.ValidationError("Введён некорректный период действия.")
        if attrs['quantity_lessons_max'] == 0 and attrs['is_unlimited'] is False:
            raise serializers.ValidationError("Установите максимальное количество уроков,"
                                              " или активируйте поле 'Безлимитный'")
        return attrs