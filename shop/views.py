import hashlib

#http://ccbv.co.uk
from django.views.generic import ListView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from epayco.models import EpayCo
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'shop/item_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ItemListView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return self.get(request, args, kwargs)


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
def carShopSecurity(request):
    template_name = 'shop/car_shop_security.html'
    items = request.POST.getlist('item', [])
    queryset = Item.objects.filter(pk__in=items)

    epayco = EpayCo.objects.first()

    p_description = 'demo-app-co ePayCo'

    p_cust_id_cliente = epayco.client_id
    p_key = epayco.p_key
    p_id_invoice = ''
    p_amount = queryset.aggregate(Sum('price'))['price__sum']
    p_currency_code = epayco.p_currency_code

    signature = '{0}^{1}^{2}^{3}^{4}'.format(
                p_cust_id_cliente,
                p_key,
                p_id_invoice,
                p_amount,
                p_currency_code
            )

    h = hashlib.md5()
    h.update(signature.encode('utf-8'))
    p_signature = h.hexdigest()

    p_tax = 0
    p_amount_base = 0
    p_test_request = 'TRUE' if epayco.test else 'FALSE'

    p_url_response = epayco.url_response
    p_url_confirmation = epayco.url_confirmation

    context = {
            'p_cust_id_cliente': p_cust_id_cliente,
            'p_key': p_key,
            'p_id_invoice': p_id_invoice,
            'p_amount': p_amount,
            'p_currency_code': p_currency_code,
            'p_signature': p_signature,
            'p_tax': p_tax,
            'p_amount_base': p_amount_base,
            'p_test_request': p_test_request,
            'p_url_response': p_url_response,
            'p_url_confirmation': p_url_confirmation,
            'p_description': p_description
    }

    return render_to_response(template_name, context)


@require_POST
@csrf_exempt
def confirmation_view(request):
    print(request.POST)
    return HttpResponse('')
