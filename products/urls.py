from django.urls import path
from django.conf.urls import url
from .views import AddProduct
from . import views

urlpatterns = [
    path('add/', AddProduct.add_product, name='add_product'),
    url(r'edit/(?P<pk>\d+)/$', AddProduct.edit_product, name='edit_product'),

]
