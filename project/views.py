from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Config, Project
from project.serializers import ConfigSerializer, ProjectSerializer, ProjectUserSerializer

from system.serializers import UserProfileSerializer


# Create your views here.
@extend_schema(tags=["Project"])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @extend_schema(responses=ProjectUserSerializer(many=True))
    @action(methods=["GET"], detail=False)
    def get_all_project(self, request):
        project_list = Project.objects.all()
        page = self.paginate_queryset(project_list)
        if page:
            serializer = ProjectUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProjectUserSerializer(project_list, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProjectSerializer(many=True))
    @action(methods=["GET"], detail=False)
    def get_single_user_project(self,request):
        project_list = Project.objects.filter(project_leader=request.user) | Project.objects.filter(user_list=request.user)
        project_list = project_list.distinct()
        page = self.paginate_queryset(project_list)
        if page:
            serializer = ProjectSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProjectSerializer(project_list,many=True)
        return Response(serializer.data)



@extend_schema(tags=["Project"])
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
