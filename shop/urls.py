from django.conf.urls import url
from .views import ItemListView, CarShopListView
from .views import confirmation_view, carShopSecurity

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='item_list'),
    url(r'^car-shop$', CarShopListView.as_view(), name='car_shop'),
    url(r'^car-shop/generate$', carShopSecurity, name='car_shop_security'),
    url(r'^confirmation$', confirmation_view, name='confirmation'),
]
