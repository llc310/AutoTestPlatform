from django.contrib import admin

from case_ui.models import (
    Action,
    CaseUI,
    CaseUIAction,
    Element,
    KeyWord,
)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "by", "path", "project_id")
    search_fields = ("name", "path")


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id", "keyword_name")
    search_fields = ("keyword_name",)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "allure", "parametrize", "validate")


@admin.register(CaseUI)
class CaseUIAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_id")
    search_fields = ("name",)


@admin.register(CaseUIAction)
class CaseUIStepAdmin(admin.ModelAdmin):
    list_display = ("id", "caseui_id", "action_id", "sort")
    list_filter = ("caseui_id",)
    ordering = ("caseui_id", "sort")
