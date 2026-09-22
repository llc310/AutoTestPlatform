from rest_framework import routers

from suite.views import RunResultViewSet, SuiteViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("suite", SuiteViewSet)
router.register("runresult", RunResultViewSet)

urlpatterns += router.urls
