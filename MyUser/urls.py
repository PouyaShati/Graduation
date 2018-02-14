from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^panel/$', views.user_panel, name='user_panel'),
    url(r'^.*/', views.handle404, name='handle404')
]