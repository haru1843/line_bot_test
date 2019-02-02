from django.conf.urls import url

from . import views

app_name = 'char_moon'

urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^callback$', views.callback, name="callback"),
    url(r'^disp_moon$', views.disp_moon, name="disp_moon"),
    url(r'^identify_request$', views.identify_request, name="identify_request"),
    # url(r'^webhook$', views.webhook, name="webhook"),
]