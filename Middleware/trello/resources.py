# trello/resource.py
from trello.models import Workspace
from import_export import resources, fields
from import_export.admin import ImportMixin


# IMPORT_EXPORT Settings
class WorkspaceResource(resources.ModelResource):
    trello_id = fields.Field(column_name='id')
    display_name = fields.Field(column_name='displayName')
    description = fields.Field(column_name='desc')
    class Meta:
        model = Workspace
