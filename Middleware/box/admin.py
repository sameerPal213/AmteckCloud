from django.contrib import admin
from .models import ProjectFolders, FolderSearchTerm

# Register your models here.
@admin.register(ProjectFolders)
class ProjectFoldersAdmin(admin.ModelAdmin):
    search_fields = ['sta']
    list_filter = ['sta']

@admin.register(FolderSearchTerm)
class FolderSearchTermAdmin(admin.ModelAdmin):
    search_fields = ['folder', 'search_term']
    list_filter = ['folder', 'search_term']
