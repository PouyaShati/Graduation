from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.admin_signup, name='admin_signup'),
    url(r'^login/$', views.admin_login, name='admin_login'),
    url(r'^logout/$', views.admin_logout, name='admin_logout'),
    url(r'^panel/$', views.admin_panel, name='admin_panel'),
]