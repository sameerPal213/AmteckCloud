from django.contrib import admin
from menu_app.models import MenuItem

# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'icon')
    search_fields = ('title', 'parent', 'url')
