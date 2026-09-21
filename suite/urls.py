from rest_framework import routers

from suite.views import SuiteViewSet, RunResultViewSet

urlpatterns = [

]

router = routers.SimpleRouter()
router.register("suite",SuiteViewSet)
router.register("runresult",RunResultViewSet)

urlpatterns += router.urls