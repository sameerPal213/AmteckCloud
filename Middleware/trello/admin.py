# trello/admin.py
from django.contrib import admin
from .models import Member, Enterprise, Workspace, Board, Label, List, Card, Webhook
from trello.resources import WorkspaceResource
from import_export.admin import ImportMixin



# Register your models here
admin.site.register(Member)
admin.site.register(Enterprise)
@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    fields = ["description", "trello_id", "model_id"]
    list_display = ["description", "trello_id", "model_id"]

@admin.register(Workspace)
class WorkspaceAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('display_name', 'enterprise', )
    search_fields = ['display_name', ]

    resource_class = WorkspaceResource
admin.site.register(Board)
admin.site.register(Label)
admin.site.register(List)
admin.site.register(Card)
