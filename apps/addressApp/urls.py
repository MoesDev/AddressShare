from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^sessions_address/$', views.sessions_address, name="sessions_address"),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
]