from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.student_signup, name='student_signup'),
    url(r'^login/$', views.student_login, name='student_login'),
    url(r'^logout/$', views.student_logout, name='student_logout'),
    url(r'^panel/$', views.student_panel, name='student_panel'),
    url(r'^perform_task/(?P<task_id>\d*/?)$', views.perform_task, name='perform task'),
    url(r'^perform_process/(?P<process_blueprint_name>\w*)/$', views.perform_process, name='perform process'),
    url(r'^graduate/$', views.graduate, name='graduate'),
    url(r'^process_page/(?P<student_id>\d*/?)/(?P<process_id>\d*)/?$', views.process_page, name='process_page'),
    url(r'^form_page/(?P<student_id>\d*/?)/(?P<form_id>\d*)/?$', views.form_page, name='form_page'),
    url(r'^form_page/(?P<student_id>\d*/?)/(?P<payment_id>\d*)/?$', views.payment_page, name='payment_page')
    # url(r'^.*/$', views.student_404, name='student_404'),
]