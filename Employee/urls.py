from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^employee_signup/$', views.employee_signup, name='employee_signup'),
    url(r'^employee_login/$', views.employee_login, name='employee_login'),
    url(r'^employee_logout/$', views.employee_logout, name='employee_logout'),
    url(r'^employee_panel/$', views.employee_panel, name='employee_panel'),
]