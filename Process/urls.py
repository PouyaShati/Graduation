from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_process_blueprint/$', views.create_process_blueprint, name='create_process_blueprint'),
    url(r'^create_employee_task_blueprint/$', views.create_employee_task_blueprint, name='create_employee_task_blueprint'),
    url(r'^create_form_blueprint/$', views.create_form_blueprint, name='create_form_blueprint'),
    url(r'^create_payment_blueprint/$', views.create_payment_blueprint, name='create_payment_blueprint'),
    url(r'^create_question_set/$', views.create_question_set, name='create_question_set'),
    # url(r'^process_blueprint_page/(?P<name>([a-z][0-9])*)/$', views.process_blueprint_page, name='process_blueprint_page'),
    url(r'^process_blueprint_page/(?P<id>\w*)/(?P<action>\w*)/?$', views.process_blueprint_page, name='process_blueprint_page'),
    url(r'^question_set_page/(?P<id>\w*)/(?P<action>\w*)/?$', views.question_set_page, name='question_set_page'),

]