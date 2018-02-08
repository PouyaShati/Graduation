from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^employee_signup/$', views.employee_signup, name='employee_signup'),
    url(r'^employee_login/$', views.employee_login, name='employee_login'),
    url(r'^employee_logout/$', views.employee_logout, name='employee_logout'),
    url(r'^employee_panel/$', views.employee_panel, name='employee_panel'),
    url(r'^add_department/$', views.add_department, name='add_department'),
    url(r'^department_panel/(?P<department_id>\d*/?)/(?P<action>\w*/?)$', views.department_panel, name='department_panel'),
    url(r'^perform_task/(?P<task_id>\d*/?)$', views.perform_task, name='perform task'),
    url(r'^add_task/(?P<task_bp_name>\w*/?)$', views.add_task, name='add task'),
]