from pathlib import Path

import time

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from case_api.models import CaseAPI as CaseAPI
from suite.models import Suite, RunResult
from suite.serializers import SuiteSerializer, RunResultSerializer


# Create your views here.
@extend_schema(
    tags=["Suite"]
)
class SuiteViewSet(viewsets.ModelViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer

    @action(methods=["POST"])
    def run(self,request,pk):
        suite = self.get_object()
        result = suite.run()
        return Response({
            "id": pk,
            "result": result
        })

class RunResultViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = RunResult.objects.all()
    serializer_class = RunResultSerializer