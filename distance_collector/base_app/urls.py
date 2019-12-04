from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.collecting_data_view, name='collecting_data_view'),
]
