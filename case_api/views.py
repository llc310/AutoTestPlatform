from rest_framework import viewsets

from case_api.models import Case, Endpoint
from case_api.serializers import CaseSerializer, EndpointSerializer


# Create your views here.
class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
