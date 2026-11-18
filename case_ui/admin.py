from django.contrib import admin

from case_ui.models import (
    Action,
    CaseUI,
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
    list_display = ("id", "name", "allure")


@admin.register(CaseUI)
class CaseUIAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_id", "action_list")
    search_fields = ("name",)
