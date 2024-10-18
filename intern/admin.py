from django.contrib import admin
from .models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'role', 'joined_at')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Users.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(InternProfile)
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'teacher', 'department', 'internship_period', 'is_active', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Users.objects.filter(role='intern')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HrProfile)
class HrProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Users.objects.filter(role='hr')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ChiefProfile)
class ChiefProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Users.objects.filter(role='chief')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'intern', 'rated_by', 'created_at')

@admin.register(PDFInformation)
class PDFInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
