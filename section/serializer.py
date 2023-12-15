from rest_framework import serializers

from section.models import SectionModel
from users.models import UserModel
from users.serializer import UserModelSerializer


class SectionSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    owner = UserModelSerializer(many=True, read_only=True)
    # trainers = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, required=False)
    trainers = UserModelSerializer(many=True, read_only=True)
    students = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, required=False)

    class Meta:
        model = SectionModel
        fields = ('id', 'name', 'owner', 'trainers', 'students', 'created_at', 'updated_at',)
