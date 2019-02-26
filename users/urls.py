from django.urls import path
from django.conf.urls import url
from .views import SignupView, EditUserDataView
from . import views

urlpatterns = [
    path('signup/', SignupView.signup, name='signup'),
    url(r'edit/(?P<pk>\d+)/$', EditUserDataView.as_view(), name="edit"),
    url(r'^activate/(?P<pk>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        SignupView.activate, name='activate'),
]
