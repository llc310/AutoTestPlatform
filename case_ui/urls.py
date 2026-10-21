from rest_framework import routers

from case_ui.views import CaseUIViewSet, ElementViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("element", ElementViewSet)
router.register("case", CaseUIViewSet)

urlpatterns += router.urls
