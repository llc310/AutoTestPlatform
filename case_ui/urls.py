from rest_framework import routers

from case_ui.views import CaseViewSet, ElementViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("element", ElementViewSet)
router.register("case", CaseViewSet)

urlpatterns += router.urls
