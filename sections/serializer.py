from rest_framework import serializers

from sections.models import GroupModel, SectionModel
from users.models import StudentModel, TrainerModel
from users.serializer import UserModelSerializer, TrainerModelSerializer


class SectionSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner',
        queryset=TrainerModel.objects.all(),
        write_only=True
    )
    trainers_ids = serializers.PrimaryKeyRelatedField(
        source='trainers',
        queryset=TrainerModel.objects.all(),
        write_only=True,
        required=False,
        many=True
    )
    students_ids = serializers.PrimaryKeyRelatedField(
        source='students',
        queryset=StudentModel.objects.all(),
        write_only=True,
        required=False,
        many=True
    )

    owner = UserModelSerializer(read_only=True)
    trainers = TrainerModelSerializer(many=True, read_only=True)
    students = UserModelSerializer(many=True, read_only=True)

    class Meta:
        model = SectionModel
        fields = ('id', 'name', 'owner', 'owner_id', 'trainers', 'trainers_ids',
                  'students', 'students_ids', 'created_at', 'updated_at',)


class GroupSerializer(serializers.ModelSerializer):
    trainers = UserModelSerializer(many=True, read_only=True)
    students = UserModelSerializer(many=True, read_only=True)

    class Meta:
        model = GroupModel
        fields = ('id', 'name', 'section', 'trainers', 'students',
                  'created_at', 'updated_at')
