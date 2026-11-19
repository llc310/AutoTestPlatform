from django.views.static import serve
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from suite.models import RunResult, Suite
from suite.serializers import RunResultSerializer, SuiteSerializer


# Create your views here.
@extend_schema(tags=["Suite"])
@api_view()
@permission_classes([permissions.AllowAny])
def static_server(request, path, document_root=None, show_indexes=False):
    response = serve(request, path, document_root)
    if ".yaml" in path:
        response.headers["Content-Type"] = "text/yaml;charset=utf-8"
    elif ".log" in path:
        response.headers["Content-Type"] = "text/plain;charset=utf-8"
    return response


@extend_schema(tags=["Suite"])
class SuiteViewSet(viewsets.ModelViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer

    @extend_schema(responses=SuiteSerializer(many=True))
    @action(methods=["GET"],detail=False)
    def get_single_suite(self,request):
        suite_list = Suite.objects.filter(project_id=request.query_params["project_id"])
        page = self.paginate_queryset(suite_list)
        if page:
            serializer = SuiteSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SuiteSerializer(suite_list, many=True)
        return Response(serializer.data)


    @action(methods=["POST"], detail=True)
    def run(self, request, pk):
        suite = self.get_object()

        if suite.run_type == Suite.RunType.ONCE:
            suite.run()
            return Response({"id": pk, "result": "该用例只执行一次"})
        else:
            return Response({"id": pk, "result": "该用例无需手动执行，会定时执行"})

    @action(
        methods=["POST", "GET"], detail=True, permission_classes=[permissions.AllowAny]
    )
    def webhook(self, request: Request, pk):
        suite = self.get_object()
        hook_key = request.query_params.get("key")

        if suite.run_type == Suite.RunType.WEBHOOK:
            if suite.hook == hook_key:
                suite.run()
                return Response({"id": pk, "result": "该用例使用webhook执行"})
            else:
                return Response({"id": pk, "result": "该测试套件的hook密钥错误"})
        else:
            return Response({"id": pk, "result": "该测试套件不适用webhook执行"})


@extend_schema(tags=["Suite"])
class RunResultViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RunResult.objects.all()
    serializer_class = RunResultSerializer

    @extend_schema(responses=RunResultSerializer(many=True))
    @action(methods=["GET"],detail=False)
    def get_single_runresult(self,request):
        runresult_list = RunResult.objects.filter(suite=request.query_params["suite_id"])
        page = self.paginate_queryset(runresult_list)
        if page:
            serializer = RunResultSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RunResultSerializer(runresult_list,many=True)
        return Response(serializer.data)