from django.contrib import admin

from case_ui.models import Element, CaseUIInfo, CaseUI


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project")


@admin.register(CaseUIInfo)
class CaseUIInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(CaseUI)
class CaseUIAdmin(admin.ModelAdmin):
    list_display = ("id", "project")
