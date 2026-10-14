from django.contrib.auth.models import User
from rest_framework import serializers

from system.models import Department, Position, Role


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="profile.name", read_only=True)
    head_img = serializers.CharField(source="profile.head_img",read_only=True)

    class Meta:
        model = User
        fields = ["id","name","head_img"]

class DepartmentSerializer(serializers.ModelSerializer):
    leader = UserProfileSerializer(read_only=True)

    class Meta:
        model = Department
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    user_detail = UserProfileSerializer(source="user", read_only=True)
    department_detail = DepartmentSerializer(source="department", read_only=True)
    position_detail = PositionSerializer(source="position", read_only=True)


    class Meta:
        model = Role
        fields = [
            "id",
            "user",
            "department",
            "position",
            "user_detail",
            "department_detail",
            "position_detail",
        ]
        extra_kwargs = {
            "user": {"write_only": True},
            "department": {"write_only": True},
            "position": {"write_only": True},
        }
