from django.conf.urls import url

from . import views

app_name = 'char_moon'

urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^callback$', views.callback, name="callback"),
    url(r'^char_moon$', views.char_moon, name="char_moon"),
    # url(r'^webhook$', views.webhook, name="webhook"),
]