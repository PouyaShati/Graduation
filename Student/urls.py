from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^student_signup/$', views.student_signup, name='student_signup'),
]