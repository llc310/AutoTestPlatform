from rest_framework import routers

from case_api.views import CaseAPIInfoViewSet, CaseAPIViewSet, EndpointViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("endpoint", EndpointViewSet)
router.register("case_api_info", CaseAPIInfoViewSet)
router.register("case_api", CaseAPIViewSet)

urlpatterns += router.urls
