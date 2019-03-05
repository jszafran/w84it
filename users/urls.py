from django.urls import path
from django.conf.urls import url
from .views import SignupView, EditUserDataView, DeletionView

urlpatterns = [
    path('signup/', SignupView.signup, name='signup'),
    url(r'edit/(?P<pk>\d+)/$', EditUserDataView.as_view(), name="edit"),
    url(r'^activate/(?P<pk>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        SignupView.activate, name='activate'),
    url(r'delete_user/revert', DeletionView.revert_deletion, name='revert_user_deletion'),
    url(r'delete_user/', DeletionView.delete_user, name='delete_user'),

]
