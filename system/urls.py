from rest_framework import routers


from system.views import DepartmentViewSet, PositionViewSet, RoleViewSet

urlpatterns = [

]

router = routers.SimpleRouter()
router.register("department",DepartmentViewSet)
router.register("position",PositionViewSet)
router.register("role",RoleViewSet)

urlpatterns += router.urls