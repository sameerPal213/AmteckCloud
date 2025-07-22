from django.contrib import admin
from .models import (Skill, User, Assessment, Category)

# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'max_score')
    list_filter = ('category__name', 'order')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job', 'is_assessor')
    list_filter = ('job_title', 'is_assessor', 'job')
    search_fields = ('first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'is_assessor', 'job')}),
    )


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('recorded_at','user', 'assessor', 'job')
    list_filter = ('recorded_at', 'assessor', 'is_self_assessment')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
