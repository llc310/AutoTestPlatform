from django.contrib import admin

from system.models import Department, Position, Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "leader", "description")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_leader")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "department", "position")
