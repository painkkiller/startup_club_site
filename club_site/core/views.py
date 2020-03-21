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
    can_edit = False
    if request.user in project.founders.all():
        can_edit = True
    context = { 'project': project, 'can_edit': can_edit }
    return render(request, 'projectdetails.html', context)

def project_edit(request, slug):
    print('project_edit', slug)
    if request.method == 'POST':
        if slug == 'new':
            projectForm = EditProjectForm(request.POST, request.user)
        else:
            project = Project.objects.get(slug=slug)
            projectForm = EditProjectForm(request.POST, instance=project)
        if projectForm.is_valid():
            print('project_edit0')
            project = projectForm.save()
            #project.founders.set(request.user)
            project.save()
            print('project_edit2', project)
            messages.success(request, ('Вы успешно отредактировали свой проект'))
            return redirect('project_details', slug=project.slug)
        else:
            messages.error(request, ('Какие то ошибки не дают сохранить проект'))
            context = { 'form': projectForm, 'slug': slug }
            return render(request, 'projectedit.html', context)
    else:
        if slug == 'new':
            form = EditProjectForm()
        else:
            project = Project.objects.get(slug=slug)
            print('project_edit', project)
            form = EditProjectForm(instance=project)
        context = { 'form': form, 'slug': slug }
        return render(request, 'projectedit.html', context)