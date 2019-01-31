from django.conf.urls import url

from . import views

app_name = 'char_moon'

urlpatterns = [
    url(r'^callback$', views.callback, name="callback"),
]