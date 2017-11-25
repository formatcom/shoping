from django.conf.urls import url
from .views import ItemListView, CarShopListView, confirmation_view

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='item_list'),
    url(r'^car-shop$', CarShopListView.as_view(), name='car_shop'),
    url(r'^confirmation$', confirmation_view, name='confirmation'),
]
