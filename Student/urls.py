from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.student_signup, name='student_signup'),
    url(r'^login/$', views.student_login, name='student_login'),
    url(r'^logout/$', views.student_logout, name='student_logout'),
    url(r'^panel/$', views.student_panel, name='student_panel'),
    url(r'^perform_task/(?P<task_id>\d*/?)$', views.perform_task, name='perform task'),
    url(r'^.*/$', views.student_404, name='student_404')
]