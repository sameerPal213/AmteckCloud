from django.db import models
from coins.models import Project

# Create your models here.

class ProjectFolders(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sta = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Project Folder"
        verbose_name_plural = "Project Folders"
        ordering = ['sta']
        managed = True
        db_table = "Bronze].[project_folders"


class FolderSearchTerm(models.Model):
    folder = models.CharField(max_length=100)
    search_term = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Folder Search Term"
        verbose_name_plural = "Folder Search Terms"
        managed = True
        db_table = "Bronze].[folder_search_terms"
