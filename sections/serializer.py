from rest_framework import serializers

from sections.models import GroupModel, SectionModel
from users.models import UserModel
from users.serializer import UserModelSerializer


class SectionSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner',
        queryset=UserModel.objects.all(),
        write_only=True
    )
    trainers_ids = serializers.PrimaryKeyRelatedField(
        source='trainers',
        queryset=UserModel.objects.all(),
        write_only=True,
        required=False,
        many=True
    )
    students_ids = serializers.PrimaryKeyRelatedField(
        source='students',
        queryset=UserModel.objects.all(),
        write_only=True,
        required=False,
        many=True
    )

    owner = UserModelSerializer(read_only=True)
    trainers = UserModelSerializer(many=True, read_only=True)
    students = UserModelSerializer(many=True, read_only=True)

    class Meta:
        model = SectionModel
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    trainers = UserModelSerializer(many=True, read_only=True)
    students = UserModelSerializer(many=True, read_only=True)

    class Meta:
        model = GroupModel
        fields = ('id', 'name', 'section', 'trainers', 'students',
                  'created_at', 'updated_at')
