from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.log_out, name='logout'),
]