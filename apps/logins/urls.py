from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.registrationPage, name="index"),
    url(r'^user/register$', views.register, name="register"),
    url(r'^user/login$', views.login, name="login"),
    url(r'^user/success/$', views.success, name="success"),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
    url(r'^signout$', views.signout, name="signout"),
    url(r'^not_signed_in/$', views.not_signed_in, name="not_signed_in"),

]