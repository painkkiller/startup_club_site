from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import EditProjectForm
from .models import Project



def home(request):
    return render(request, 'index.html')

def projects(request):
    projects = Project.objects.all()
    context = { 'projects': projects }
    return render(request, 'projectslist.html', context)

def project_details(request, slug):
    project = Project.objects.get(slug=slug)
    context = { 'project': project }
    return render(request, 'projectdetails.html', context)

def project_edit(request, slug):
    if request.method == 'POST':
        projectForm = EditProjectForm(request.POST, request.user)
        if projectForm.is_valid():
            project = projectForm.save()
            #project.founders.set(request.user)
            project.save()
            print('project_edit', project)
            messages.success(request, ('Вы успешно отредактировали свой проект'))
            return redirect('project_details', slug=project.slug)
        else:
            messages.error(request, ('Какие то ошибки не дают сохранить проект'))
            context = { 'form': projectForm }
            return render(request, 'projectedit.html', context)
    else:
        if slug == 'new':
            form = EditProjectForm()
        else:
            project = Project.objects.get(slug=slug)
            print('project_edit', project)
            form = EditProjectForm(instance=project)
        context = { 'form': form }
        return render(request, 'projectedit.html', context)