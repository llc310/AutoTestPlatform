from rest_framework import routers

from case_ui.views import ElementViewSet, KeyWordViewSet, ActionViewSet, AllureViewSet, ParametrizeViewSet, \
    ValidateViewSet, StepViewSet, CaseUIViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register("element", ElementViewSet)
router.register("keyword", KeyWordViewSet)
router.register("allure",AllureViewSet)
router.register("parametrize",ParametrizeViewSet)
router.register("validate",ValidateViewSet)
router.register("step",StepViewSet)
router.register("action",ActionViewSet)
router.register("case",CaseUIViewSet)

urlpatterns += router.urls
