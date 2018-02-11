from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.employee_signup, name='employee_signup'),
    url(r'^login/$', views.employee_login, name='employee_login'),
    url(r'^logout/$', views.employee_logout, name='employee_logout'),
    url(r'^panel/$', views.employee_panel, name='employee_panel'),
    url(r'^add_department/$', views.add_department, name='add_department'),
    url(r'^department_panel/(?P<department_id>\d*/?)/(?P<action>\w*/?)$', views.department_panel, name='department_panel'),
    url(r'^perform_task/(?P<task_id>\d*/?)$', views.perform_task, name='perform task'),
    url(r'^add_task/(?P<task_bp_name>\w*/?)$', views.add_task, name='add task'),
    url(r'^all_employees_list/$', views.all_employees_list, name='all_employees_list'),
    url(r'^all_departments_list/$', views.all_departments_list , name='all_departments_list'),
    # url(r'^.*/$', views.employee_404, name='employee_404')
]