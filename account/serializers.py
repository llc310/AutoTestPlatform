from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from account.models import Profile
from system.models import Role


@extend_schema_serializer(component_name="UserRole")
class RoleSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    position = serializers.CharField(source="position.name")
    is_leader = serializers.CharField(source="position.is_leader")

    class Meta:
        model = Role
        fields = ["department", "position", "is_leader"]


class ProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    role_list = RoleSerializer(read_only=True, many=True, source="get_role_list")

    class Meta:
        model = Profile
        fields = "__all__"

    def get_token(self, obj):
        user = obj.user
        token, is_create = Token.objects.get_or_create(user=user)
        return token.key

    def get_user(self, obj):
        return obj.user.id


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("用户名或密码不正确")
        Profile.objects.get_or_create(user=user)
        Token.objects.get_or_create(user=user)
        attrs["user"] = user
        return attrs


class ResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_password = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]

        if new_password != confirm_password:
            raise serializers.ValidationError("两次密码不一致")
        return attrs
