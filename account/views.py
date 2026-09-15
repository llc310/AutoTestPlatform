from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import Profile
from account.serializers import (LoginSerializer, ProfileSerializer,
                                 ResetSerializer)


# Create your views here.
@extend_schema(tags=["Account"])
class ProfileViewSet(viewsets.GenericViewSet):
    @extend_schema(
        request=LoginSerializer,
        responses=ProfileSerializer,
    )
    @action(methods=["POST"], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = Profile.objects.get(user=serializer.validated_data["user"])
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    @extend_schema(request=ResetSerializer, responses={204: None})
    @action(methods=["POST"], detail=False)
    def reset_password(self, request):
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses=ProfileSerializer)
    @action(methods=["GET"], detail=False)
    def profile(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    @action(methods=["POST"], detail=False)
    def change(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
