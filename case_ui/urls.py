from rest_framework import routers

from case_ui.views import CaseUIViewSet, ElementViewSet, CaseUIInfoViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("element", ElementViewSet)
router.register("case_ui_info",CaseUIInfoViewSet)
router.register("case", CaseUIViewSet)

urlpatterns += router.urls
