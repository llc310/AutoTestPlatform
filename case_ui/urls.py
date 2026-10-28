from rest_framework import routers

from case_ui.views import ElementViewSet, KeyWordViewSet, ActionViewSet, CaseUIViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("element", ElementViewSet)
router.register("keyword", KeyWordViewSet)
router.register("action",ActionViewSet)
router.register("case",CaseUIViewSet)

urlpatterns += router.urls
