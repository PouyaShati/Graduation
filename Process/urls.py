from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_process_blueprint/$', views.create_process_blueprint, name='create_process_blueprint'), # TODO add action
]