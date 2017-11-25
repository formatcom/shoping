#http://ccbv.co.uk
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'shop/item_list.html'


class CarShopListView(ListView):
    model = Item
    template_name = 'shop/car_shop_list.html'

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.object_list = queryset
        context = self.get_context_data()
        total = queryset.aggregate(Sum('price'))['price__sum']
        context['total'] = total
        return self.render_to_response(context)

    def get_queryset(self):
        items = self.request.POST.getlist('item', [])
        queryset = self.model.objects.filter(pk__in=items)
        return queryset


@require_POST
def confirmation_view(request):
    print(request.POST)
    return HttpResponse('')
