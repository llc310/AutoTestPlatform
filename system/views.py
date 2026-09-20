from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from system.models import Department, Position, Role
from system.serializers import (DepartmentSerializer, PositionSerializer,
                                RoleSerializer)


# Create your views here.
@extend_schema(tags=["System"])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@extend_schema(tags=["System"])
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


@extend_schema(tags=["System"])
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
