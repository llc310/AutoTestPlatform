from pathlib import Path

import time
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from case_api.models import Case as CaseAPI
from suite.models import Suite, RunResult
from suite.serializers import SuiteSerializer, RunResultSerializer


# Create your views here.
@extend_schema(
    tags=["Suite"]
)
class SuiteViewSet(viewsets.ModelViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer

class RunResultViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = RunResult.objects.all()
    serializer_class = RunResultSerializer

    @action(methods=["POST"],detail=True)
    def run_case_api(self,request,pk):
        obj = CaseAPI.objects.get(id=pk)
        path = Path(f"upload_yaml/case_api/{pk}_{time.time()}")
        path.mkdir(parents=True,exist_ok=True)