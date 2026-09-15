from rest_framework import serializers
from system.models import Department, Positon, Role


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positon
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    department_detail = DepartmentSerializer(source="department", read_only=True)
    position_detail = PositionSerializer(source="position", read_only=True)

    class Meta:
        model = Role
        fields = ["id", "user", "department", "position", "department_detail", "position_detail"]
        extra_kwargs = {
            "user": {"write_only": True},
            "department": {"write_only": True},
            "position": {"write_only": True},
        }

