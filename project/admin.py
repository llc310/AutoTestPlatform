from django.contrib import admin

from project.models import Project, Config


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_leader", "base_url", "description")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "project")
