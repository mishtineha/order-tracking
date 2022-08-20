from .views import OrderAPI, OrderUser, OrderStore
from django.urls import path
from django.conf.urls import url
urlpatterns = [
    path('', OrderAPI.as_view()),
    url(r'^users/(?P<pk>\d+)/$', OrderUser.as_view()),
    url(r'^stores/(?P<pk>\d+)/$', OrderStore.as_view())
]