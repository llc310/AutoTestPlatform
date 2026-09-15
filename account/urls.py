from django.urls import path
from django.views.static import serve
from rest_framework import routers

from account.models import app_static_path
from account.views import ProfileViewSet

urlpatterns = [path("static/<path:path>", serve, {"document_root": app_static_path})]

router = routers.SimpleRouter()
router.register("profile", ProfileViewSet, "profile")
urlpatterns += router.urls
