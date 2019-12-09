from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.collecting_data_view, name='collecting_data_view'),
    url(r'^showresult/$', views.show_result_view, name='show_result_view'),
]
