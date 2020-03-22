from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .forms import EditProjectForm
from django.contrib.auth.decorators import login_required
from .models import Project
from .mailer import mail_to_users



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

@login_required
def project_edit(request, slug):
    if request.method == 'POST':
        if slug == 'new':
            projectForm = EditProjectForm(data=request.POST, files=request.FILES)
        else:
            project = Project.objects.get(slug=slug)
            projectForm = EditProjectForm(data=request.POST, files=request.FILES, instance=project)
        if projectForm.is_valid():
            project = projectForm.save()
            project.founders.add(request.user)
            project.save()
            current_site = get_current_site(request)
            mail_creation_helper(slug == 'new', request.user, project, current_site.domain)
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
            form = EditProjectForm(instance=project)
        context = { 'form': form, 'slug': slug }
        return render(request, 'projectedit.html', context)

def mail_creation_helper(is_new, user, project, domain):
    if is_new:
        subject_mail = 'Ваш проект создан'
        html_message = render_to_string('emails/addedtoproject.html', {
            'user': user,
            'domain': domain,
            'project': project,
        })
        txt_message = render_to_string('emails/addedtoproject.html', {
            'user': user,
            'domain': domain,
            'project': project,
        })
    else:
        subject_mail = 'Ваш проект отредактирован'
        html_message = render_to_string('emails/editedproject.html', {
            'user': user,
            'domain': domain,
            'project': project,
        })
        txt_message = render_to_string('emails/editedproject.txt', {
            'user': user,
            'domain': domain,
            'project': project,
        })
    mails = [ founder.email for founder in project.founders.all()]
    resp = mail_to_users(subject_mail, html_content= html_message, txt_content=txt_message, mails=mails)
    return resp
