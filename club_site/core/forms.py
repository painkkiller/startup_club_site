from django import forms
from .models import Project, Vacancy, PROJECT_STATUS_CHOICES, VACANCY_TYPE_CHOICES, SPECIALTIES_TYPES
from django.contrib.auth import get_user_model
from django_comments.forms import CommentForm
from django_comments.models import Comment

print(CommentForm)


User = get_user_model()


class EditProjectForm(forms.ModelForm):
    title =  forms.CharField(label="Название проекта", help_text="<small></small>", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}))
    description = forms.CharField(label="Описание", help_text="<small>краткое описание вашего проекта, не больше 2000 знаков</small>", max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control',}))
    slug = forms.CharField(label="ЧПУ", help_text="<small>Человекочитаемый url для SEO, вида best-startup-ever</small>", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}))
    site = forms.CharField(label="Сайт", help_text="<small>сайт вашего проекта (если есть)</small>", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}), required=False)
    status = forms.ChoiceField(choices = PROJECT_STATUS_CHOICES, label="Стадия проекта", widget=forms.Select(attrs={'class': 'form-control',}), required=True)
    founders = forms.ModelMultipleChoiceField(queryset = User.objects.all(), label="Основатели", widget=forms.SelectMultiple(attrs={'class': 'form-control',}), required=True)
    preza = forms.FileField(label="Презентация", help_text="<small>презентация вашего проекта (если есть)</small>",  widget=forms.ClearableFileInput(attrs={ 'class': 'form-control-file', 'multiple': False }), required=False)
    video_pitch = forms.CharField(label="Видео", help_text="<small>Видеоссылка на YouTube питча вашего проекта или проморолик (если есть)</small>", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}), required=False)

    class Meta:
        model = Project
        fields = ('title', 'description', 'slug', 'status', 'founders', 'site', 'preza', 'video_pitch')

class ProjectCommentForm(CommentForm):
    #comment = forms.CharField(label="", help_text="", max_length=3000, widget=forms.Textarea(attrs={'class': 'form-control' }))

    def __init__(self, *args, **kwargs):
        super(ProjectCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})




class EditVacancyForm(forms.ModelForm):
    title =  forms.CharField(label="Название вакансии", help_text="<small></small>", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}))
    body = forms.CharField(label="Описание вакансии", help_text="<small>краткое описание вакансии, не больше 1000 знаков</small>", max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control',}))
    specialty = forms.ChoiceField(choices = SPECIALTIES_TYPES, label="Специальность", widget=forms.Select(attrs={'class': 'form-control',}), required=True)
    vacancy_type = forms.ChoiceField(choices = VACANCY_TYPE_CHOICES, label="Тип вакансии", widget=forms.Select(attrs={'class': 'form-control',}), required=True)

    def __init__(self, user, *args, **kwargs):
        super(EditVacancyForm, self).__init__(*args, **kwargs)
        # print('--init--', [(project.id, project.title) for project in User.objects.get(pk=5).project_set.all()])
        self.fields['project'] = forms.ModelChoiceField(queryset=User.objects.get(pk=user.id).project_set.all(), empty_label=None, to_field_name="title", label="Проект", widget=forms.Select(attrs={'class': 'form-control',}), required=True)
        self.fields['author'] = forms.ModelChoiceField(queryset=User.objects.filter(pk = user.id), initial= User.objects.get(pk = user.id), to_field_name="username", label="Автор", widget=forms.Select(attrs={'class': 'form-control',}), required=True)

    class Meta:
        model = Vacancy
        fields = ('title', 'body', 'project', 'specialty', 'author', 'vacancy_type')