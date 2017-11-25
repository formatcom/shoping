import hashlib

#http://ccbv.co.uk
from django.views.generic import ListView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from decimal import Decimal
from epayco.models import EpayCo
from ticket.models import Ticket, Status
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
def carShopSecurity(request):
    template_name = 'shop/car_shop_security.html'
    items = request.POST.getlist('item', [])
    queryset = Item.objects.filter(pk__in=items)

    epayco = EpayCo.objects.first()

    ticket = Ticket()
    ticket.total = queryset.aggregate(Sum('price'))['price__sum']
    ticket.status = Status(Status.PENDING)
    ticket.save()
    ticket.items.set(queryset)

    p_description = 'demo-app-co ePayCo'

    p_cust_id_cliente = epayco.client_id
    p_key = epayco.p_key
    p_id_invoice = '%s' % ticket.pk
    p_amount = '%s' % ticket.total
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
    epayco = EpayCo.objects.first()

    x_signature = request.POST.get('x_signature')

    x_cust_id_cliente = request.POST.get('x_cust_id_cliente')
    x_key = epayco.p_key
    x_id_invoice = request.POST.get('x_id_invoice')
    x_ref_payco = request.POST.get('x_ref_payco')
    x_transaction_id = request.POST.get('x_transaction_id')
    x_amount = request.POST.get('x_amount')
    x_currency_code = request.POST.get('x_currency_code')

    x_cod_response = request.POST.get('x_cod_response')

    signature = '{0}^{1}^{2}^{3}^{4}^{5}'.format(
                x_cust_id_cliente,
                x_key,
                x_ref_payco,
                x_transaction_id,
                x_amount,
                x_currency_code
            )

    h = hashlib.sha256()
    h.update(signature.encode('utf-8'))
    v_signature = h.hexdigest()

    ticket = Ticket.objects.filter(pk=int(x_id_invoice)).first()

    if (ticket and
        v_signature == x_signature and
        ticket.total == Decimal(x_amount):

        ticket.status = Status(int(x_cod_response))
        ticket.save()
        return HttpResponse('Gracias por su compra')
    else:
        ticket.status = Status(Status.FAILED)
        ticket.save()
        return HttpResponse('Firma invalida')

