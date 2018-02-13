from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.operator_signup, name='operator_signup'),
    url(r'^login/$', views.operator_login, name='operator_login'),
    url(r'^logout/$', views.operator_logout, name='operator_logout'),
    url(r'^panel/$', views.operator_panel, name='operator_panel'),
    url(r'^delete_department/(?P<department_id>\d*/?)$', views.delete_department, name='delete department'),
    url(r'^delete_employee/(?P<employee_id>\d*/?)$', views.delete_employee, name='delete employee'),
    url(r'^delete_student/(?P<student_id>\d*/?)$', views.delete_student, name='delete student'),
    url(r'^delete_task_blueprint/(?P<task_id>\d*/?)$', views.delete_task_blueprint, name='delete task blueprint'),
    url(r'^delete_process_blueprint/(?P<process_id>\d*/?)$', views.delete_process_blueprint, name='delete process blueprint'),

    # url(r'^.*/$', views.operator_404, name='operator_404')
]