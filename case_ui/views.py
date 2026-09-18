from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from case_ui.models import Case, Element
from case_ui.serializers import CaseUISerializer, ElementSerializer


# Create your views here.
@extend_schema(tags=["Case_UI"])
class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


@extend_schema(tags=["Case_UI"])
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseUISerializer
