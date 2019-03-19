from django.urls import path
from django.conf.urls import url
from .views import Product
from . import views

urlpatterns = [
    path('add/', Product.add_product, name='add_product'),
    url(r'edit/(?P<pk>\d+)/$', Product.edit_product, name='edit_product'),

]
