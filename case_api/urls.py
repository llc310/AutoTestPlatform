from rest_framework import routers


from case_api.views import CaseViewSet, EndpointViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("endpoint", EndpointViewSet)
router.register("case_api", CaseViewSet)

urlpatterns += router.urls