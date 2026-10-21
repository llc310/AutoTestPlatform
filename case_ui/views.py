from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from case_ui.models import Element, KeyWord
from case_ui.serializers import ElementSerializer, KeyWordSerializer


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
class KeyWordViewSet(viewsets.ModelViewSet):
    queryset = KeyWord.objects.all()
    serializer_class = KeyWordSerializer