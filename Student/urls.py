from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^student_signup/$', views.student_signup, name='student_signup'),
    url(r'^student_login/$', views.student_login, name='student_login'),
    url(r'^student_logout/$', views.student_logout, name='student_logout'),
    url(r'^student_panel/$', views.student_panel, name='student_panel'),
    url(r'^perform_payment/(?P<process_bp_name>\w*/?)/(?P<payment_bp_name>\w*/?)$', views.perform_payment, name='perform payment'),
]