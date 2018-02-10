from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.operator_signup, name='operator_signup'),
    url(r'^login/$', views.operator_login, name='operator_login'),
    url(r'^logout/$', views.operator_logout, name='operator_logout'),
    url(r'^panel/$', views.operator_panel, name='operator_panel'),
]