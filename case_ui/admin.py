from django.contrib import admin

from case_ui.models import (
    Allure,
    Action,
    CaseUI,
    CaseUIAction,
    Element,
    KeyWord,
    Parametrize,
    Step,
    Validate,
)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "by", "path", "project_id")
    search_fields = ("name", "path")


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id", "keyword_name")
    search_fields = ("keyword_name",)


@admin.register(Allure)
class AllureAdmin(admin.ModelAdmin):
    list_display = ("id", "feature", "story", "title")
    search_fields = ("feature", "story", "title")


@admin.register(Parametrize)
class ParametrizeAdmin(admin.ModelAdmin):
    list_display = ("id", "param_key")
    search_fields = ("param_key",)


@admin.register(Validate)
class ValidateAdmin(admin.ModelAdmin):
    list_display = ("id", "validate_type")
    list_filter = ("validate_type",)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "allure_id", "parametrize_id", "validate_id")


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("id", "keyword_id", "element_id", "action_id")


@admin.register(CaseUI)
class CaseUIAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_id")
    search_fields = ("name",)


@admin.register(CaseUIAction)
class CaseUIStepAdmin(admin.ModelAdmin):
    list_display = ("id", "caseui_id", "action_id", "sort")
    list_filter = ("caseui_id",)
    ordering = ("caseui_id", "sort")
