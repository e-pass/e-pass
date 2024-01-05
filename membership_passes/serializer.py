from typing import OrderedDict

from django.contrib.auth.backends import UserModel
from rest_framework import serializers, validators

from membership_passes.models import PassModel
from sections.models import SectionModel, GroupModel, LessonModel
from users.serializer import ShortUserSerializer


class ShortSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionModel
        fields = ('id', 'name')


class ShortGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ('id', 'name')


class ShortLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = ('id', 'lesson_datetime')


class PassSerializer(serializers.ModelSerializer):
    quantity_lessons_max = serializers.IntegerField(default=0)
    is_unlimited = serializers.BooleanField(default=False)
    unused_lessons = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = PassModel
        fields = ('id', 'name', 'student', 'section', 'group', 'qr_code', 'is_unlimited',
                  'quantity_lessons_max', 'unused_lessons', 'lessons',
                  'is_active', 'valid_from', 'valid_until', 'price', 'is_paid')

    def get_unused_lessons(self, instance: PassModel) -> int:
        return instance.quantity_lessons_max - len(instance.lessons.all())

    def to_representation(self, instance: PassModel) -> OrderedDict:
        ret = super(PassSerializer, self).to_representation(instance)
        if instance.is_unlimited:
            ret.pop("quantity_lessons_max")
            ret.pop("unused_lessons")
        else:
            ret.pop("is_unlimited")
        return ret


class CreatePassSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        source='student',
        queryset=UserModel.students.all(),
        read_only=False,
        write_only=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        source='section',
        queryset=SectionModel.objects.all(),
        read_only=False,
        write_only=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        source='group',
        queryset=GroupModel.objects.all(),
        read_only=False,
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

    class Meta:
        model = PassModel
        fields = ('student_id', 'section_id', 'group_id',
                  'qr_code', 'is_unlimited', 'quantity_lessons_max',
                  'valid_from', 'valid_until', 'price')

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if attrs["quantity_lessons_max"] == 0 and not attrs["is_unlimited"]:
            raise serializers.ValidationError("Установите максимальное количество уроков,"
                                              " или активируйте поле 'Безлимитный'")
        if attrs["valid_from"] > attrs["valid_until"]:
            raise serializers.ValidationError("Введён некорректный период действия.")
        return attrs


class UpdatePassSerializer(serializers.ModelSerializer):
    pass
