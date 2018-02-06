from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_process_blueprint/$', views.create_process_blueprint, name='create_process_blueprint'), # TODO add action
    url(r'^create_question_set/$', views.create_question_set, name='create_question_set'), # TODO add action
    url(r'^create_employee_task_blueprint/$', views.create_employee_task_blueprint, name='create_employee_task_blueprint'),
]