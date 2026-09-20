from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from case_api.models import CaseAPI, Endpoint, CaseAPIInfo
from case_api.serializers import CaseAPISerializer, EndpointSerializer, CaseAPIInfoSerializer


# Create your views here.
@extend_schema(tags=["Case_API"])
class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer


@extend_schema(
    tags=["Case_API"]
)
class CaseAPIInfoViewSet(viewsets.ModelViewSet):
    queryset = CaseAPIInfo.objects.all()
    serializer_class = CaseAPIInfoSerializer


@extend_schema(tags=["Case_API"])
class CaseAPIViewSet(viewsets.ModelViewSet):
    queryset = CaseAPI.objects.all()
    serializer_class = CaseAPISerializer
