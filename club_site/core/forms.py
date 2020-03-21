from django import forms
from .models import Project, PROJECT_STATUS_CHOICES
from django.contrib.auth import get_user_model

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