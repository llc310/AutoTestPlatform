from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from case_ui.models import CaseUI, Element, CaseUIInfo
from case_ui.serializers import CaseUISerializer, ElementSerializer, CaseUIInfoSerializer


# Create your views here.
@extend_schema(tags=["Case_UI"])
class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    @extend_schema(responses=ElementSerializer(many=True))
    @action(methods=["GET"],detail=False)
    def get_element(self,request):
        element_list = Element.objects.filter(project=request.query_params.get("project_id"))
        page = self.paginate_queryset(element_list)
        if page:
            serializer = ElementSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ElementSerializer(element_list, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Case_UI"])
class CaseUIInfoViewSet(viewsets.ModelViewSet):
    queryset = CaseUIInfo.objects.all()
    serializer_class = CaseUIInfoSerializer

    @extend_schema(responses=CaseUIInfoSerializer(many=True))
    @action(methods=["GET"],detail=False)
    def get_single_caseuiinfo(self,request):
        caseuiinfo_list = CaseUIInfo.objects.filter(caseuiinfo_id=request.query_params.get("caseui_id"))
        page = self.paginate_queryset(caseuiinfo_list)
        if page:
            serializer = CaseUIInfoSerializer(page,many=True)
            self.get_paginated_response(serializer.data)
        serializer = CaseUIInfoSerializer(caseuiinfo_list, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Case_UI"])
class CaseUIViewSet(viewsets.ModelViewSet):
    queryset = CaseUI.objects.all()
    serializer_class = CaseUISerializer

    @extend_schema(responses=CaseUISerializer(many=True))
    @action(methods=["GET"],detail=False)
    def get_single_case(self,request):
        case_list = CaseUI.objects.filter(project=request.query_params.get("project_id"))
        page = self.paginate_queryset(case_list)
        if page:
            serializer = CaseUISerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CaseUISerializer(case_list,many=True)
        return Response(serializer.data)