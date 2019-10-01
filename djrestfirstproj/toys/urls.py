from django.conf.urls import url
from toys import views

app_name = 'toys'

urlpatterns = [
    url(r'^toys/$', views.toy_list, name='toy_list'),
    url(r'^toys/(?P<pk>[0-9]+)$', views.toy_detail, name='toy_detail'),
]
