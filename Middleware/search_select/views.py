from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
import json
from .models import Item

# Create your views here.
class ItemListView(View):
    def get(self, request):
        items = list(Item.objects.values())
        return JsonResponse(items, safe=False)

    @method_decorator(csrf_protect)
    def post(self, request):
        data = json.loads(request.body)
        item, created = Item.objects.get_or_create(name=data['name'])
        if created:
            return JsonResponse({'status': 'created', 'item': item.id})
        else:
            return JsonResponse({'status': 'exists', 'item': item.id})


def item_form(request):
    return render(request, 'search_select/item_form.html')
