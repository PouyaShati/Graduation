from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_process_blueprint/(?P<action>\w*/?)$', views.create_process_blueprint, name='create_process_blueprint'),
]