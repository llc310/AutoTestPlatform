from rest_framework import serializers

from project.models import Config, Project
from system.serializers import UserProfileSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class ProjectUserSerializer(serializers.ModelSerializer):
    project_leader = UserProfileSerializer()
    user_list = UserProfileSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"
