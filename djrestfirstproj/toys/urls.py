from django.conf.urls import url
from toys import views

app_name = 'toys'

urlpatterns = [
    url(r'^toys/$', views.toy_list, name='toy_list'),
]
