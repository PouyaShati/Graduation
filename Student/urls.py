from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.student_signup, name='student_signup'),
    url(r'^login/$', views.student_login, name='student_login'),
    url(r'^logout/$', views.student_logout, name='student_logout'),
    url(r'^panel/$', views.student_panel, name='student_panel'),
    url(r'^perform_payment/(?P<process_bp_name>\w*/?)/(?P<payment_bp_name>\w*/?)$', views.perform_payment, name='perform payment'),
]