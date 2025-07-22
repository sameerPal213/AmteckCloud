# menu_app/context_processors.py

from menu_app.models import MenuItem

def menu(request):
    menu_items = MenuItem.objects.filter(parent=None).prefetch_related('children').order_by('title')
    return {'menu_items': menu_items}
