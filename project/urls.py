from rest_framework import routers

from project.views import ProjectViewSet, ConfigViewSet

urlpatterns = [

]
router = routers.SimpleRouter()
router.register("project",ProjectViewSet)
router.register("config",ConfigViewSet)

urlpatterns += router.urls