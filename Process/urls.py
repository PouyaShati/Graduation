from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_process_blueprint/(?P<action>\w*/?)$', views.create_process_blueprint, name='create_process_blueprint'),
    url(r'^create_employee_task_blueprint/(?P<action>\w*/?)$', views.create_employee_task_blueprint, name='create_employee_task_blueprint'),
    url(r'^create_form_blueprint/(?P<action>\w*/?)$', views.create_form_blueprint, name='create_form_blueprint'),
    url(r'^create_payment_blueprint/$', views.create_payment_blueprint, name='create_payment_blueprint'),
    url(r'^create_question_set/$', views.create_question_set, name='create_question_set'),
]