from django.urls import path
from rest_framework import routers
from AutoTestPlatform import settings
from suite.views import RunResultViewSet, SuiteViewSet, static_server

urlpatterns = [
    path("static/<path:path>",static_server,{"document_root": settings.BASE_DIR / "upload_yaml"})
]

router = routers.SimpleRouter()
router.register("suite", SuiteViewSet)
router.register("runresult", RunResultViewSet)

urlpatterns += router.urls
