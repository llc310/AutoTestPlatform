from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from case_api.models import Case, Endpoint
from case_api.serializers import CaseAPISerializer, EndpointSerializer


# Create your views here.
@extend_schema(tags=["Case_API"])
class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer


@extend_schema(tags=["Case_API"])
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseAPISerializer
