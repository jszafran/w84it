from django.urls import path
from django.conf.urls import url
from .views import ProductView
from . import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('add/', ProductView.add_product, name='add_product'),
    url(r'edit/(?P<pk>\d+)/$', ProductView.edit_product, name='edit_product'),
    url(r'delete/(?P<pk>\d+)/', ProductView.delete_product, name='delete_product'),
]
