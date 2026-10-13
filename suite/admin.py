from django.contrib import admin

from suite.models import Suite, RunResult


@admin.register(Suite)
class SuiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "run_type", "cron", "case_ui_count", "case_api_count")

    @admin.display(description="运行模式")
    def run_type(self, obj):
        return obj.get_run_type_display()


@admin.register(RunResult)
class RunResultAdmin(admin.ModelAdmin):
    list_display = ("id", "suite", "status", "is_pass", "create_datetime")

    @admin.display(description="状态")
    def status(self, obj):
        return obj.get_status_display()
