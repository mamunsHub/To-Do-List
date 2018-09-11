from django.db import models
from django import forms
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=99)

    def __str__(self):
        return self.title


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']
        labels = {'Title': 'Title of the Project'}


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=299)
    date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=(('n', 'Normal'), ('m', 'Medium'), ('h', 'High')), default='n')
    repeat = models.CharField(max_length=1, choices=(('n', 'No Repeat'), ('d', 'Daily'), ('w', 'Weekly'), ('m', 'Monthly'), ('y', 'Yearly')), default='n')

    def __str__(self):
        return self.title


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'project', 'date', 'priority', 'repeat']
        labels = {'title': 'Title', 'project': 'Project', 'date': 'Due date', 'priority': 'Priority level', 'repeat': 'Repeat'}
        widgets = {
            'date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
        }