from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from project.models import Project, Config
from project.serializers import ProjectSerializer, ConfigSerializer


# Create your views here.
@extend_schema(
    tags=["Project"]
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

@extend_schema(
    tags=["Project"]
)
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer