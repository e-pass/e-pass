from rest_framework import serializers

from section.models import SectionModel
from users.models import UserModel


class SectionSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    trainers = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, required=False)
    students = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True, required=False)

    class Meta:
        model = SectionModel
        fields = ('id', 'name', 'owner', 'trainers', 'students', 'created_at', 'updated_at',)
