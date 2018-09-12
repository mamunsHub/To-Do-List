from time import sleep
from dateutil.relativedelta import relativedelta
import datetime

from django.shortcuts import render
from django.contrib.auth.views import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Project, Task, TaskForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('projects:projects'))
    return render(request, 'projects/index.html')


@login_required
def projects(request):
    if request.method == 'POST':
        # if post method is ajax call, delete task with given ID
        if request.is_ajax():
            if request.POST['action'] == 'delete':
                task = Task.objects.get(id=request.POST['task_id'])
                task.delete()
                return JsonResponse({'deleted': True})
            # if post not ajax call, create new project
            else:
                project = Project(title=request.POST['title'].strip(), owner=request.user)
                project.save()
                return HttpResponseRedirect(reverse('projects:projects'))
    else:
        # if request get, fetch all tasks of today
        now = datetime.datetime.now()
        tasks = []
        projects = Project.objects.filter(owner=request.user).order_by('title')
        # if task date before today, mark them outdated
        for project in projects:
            task_holder = Task.objects.filter(project=project, date=now.date()).order_by('date')
            for task in task_holder:
                if task.date:
                    if task.date < datetime.date.today():
                        task.outdated = True
                    else:
                        task.outdated = False
                task.project_id = project.id
                tasks.append(task)
        context = { 'projects': projects, 'tasks': tasks }
        return render(request, 'projects/projects.html', context)


@login_required
def project(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method != 'POST':
        projects = Project.objects.filter(owner=request.user)
        tasks = Task.objects.filter(project=project).order_by('date')
        for task in tasks:
            if task.date:
                if task.date < datetime.date.today():
                    task.outdated = True
                else:
                    task.outdated = False
        add_form = TaskForm()
        context = {'projects': projects, 'project': project, 'tasks': tasks, 'add_form': add_form}

    else:
        # if ajax call for deletion, delete task with given ID
        if request.is_ajax():
            if request.POST['action'] == 'delete':
                task = Task.objects.get(id=request.POST['task_id'])
                task.delete()
        # if ajax call for add task, save form from post if valid
        elif request.POST['action'] == 'add':
            add_form = TaskForm(data=request.POST)
            if add_form.is_valid():
                add_form.save()
        return HttpResponseRedirect(reverse('projects:project', args=[project_id]))

    return render(request, 'projects/project.html', context)


@login_required
def edit_task(request, project_id, task_id):
    project = Project.objects.get(id=project_id)
    task = Task.objects.get(id=task_id)
    # if get method, send task form with current data
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        # if no repeat, delete task
        if request.is_ajax():
            if task.repeat == 'n':
                task.delete()
                sleep(.5)
                return JsonResponse({'task': 'deleted'})
            else:
                # if repeat, update task date according to repeat duration
                if not task.date:
                    task.date = datetime.datetime.now()
                if task.repeat == 'd':
                    task.date = task.date + relativedelta(days=1)
                elif task.repeat == 'w':
                    task.date = task.date + relativedelta(weeks=1)
                elif task.repeat == 'm':
                    task.date = task.date + relativedelta(months=1)
                elif task.repeat == 'y':
                    task.date = task.date + relativedelta(years=1)
                task.save()
                sleep(.5)
                return JsonResponse({'task': 'updated'})
        else:
            # if request post, save new task data
            form = TaskForm(instance=task, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('projects:project', args=[project_id]))

    context = {'form':form, 'project': project, 'task': task}
    return render(request, 'projects/edit_task.html', context)