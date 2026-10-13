from django.contrib import admin

from case_api.models import Endpoint, CaseAPIInfo, CaseAPI


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "method", "url")


@admin.register(CaseAPIInfo)
class CaseAPIInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint")


@admin.register(CaseAPI)
class CaseAPIAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project")
