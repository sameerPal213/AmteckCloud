# menuItems/models.py
from django.db import models

ICON_CHOICES = [
    ('fa-list', 'Report'),
    ('fa-user', 'User'),
    ('fa-file-contract', 'Form'),
    ('fa-chart-simple', 'Dashboard'),]
# Create your models here.
class MenuItem(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=50, null=False)
    url         = models.CharField(max_length=100, null=True, blank=True)
    parent      = models.ForeignKey("self", on_delete=models.CASCADE, null=True,
            blank=True, related_name='children', related_query_name='child')
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed     = True
        db_table    = "Bronze].[menuapp_menuitem"
