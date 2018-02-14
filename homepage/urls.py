from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.slash, name='slash'),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^.*/$', views.handle404, name='404'),
]