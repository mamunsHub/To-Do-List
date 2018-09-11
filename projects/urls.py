from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(?P<project_id>\d+)/$', views.project, name='project'),
    url(r'^projects/(?P<project_id>\d+)/tasks/$', views.project, name='project'),
    url(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
]