import logging
from django.utils.encoding import force_text
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms

from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

logger = logging.getLogger(__name__)


class EditUserForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=(""), help_text=(""))
    first_name =  forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))
    last_name =  forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['style'] = 'display: none'

    class Meta:
        model = User
        exclude = ('last_login', 'is_superuser', 'user_permissions', 'groups', 
        'password1', 'password2', 'password', 'is_staff', 'is_active', 'date_joined', 'email')

class EditProfileForm(forms.ModelForm):
    about =  forms.CharField(label="Обо мне", help_text="<small>Расскажите о себе и своих компетенциях</small>", max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control',}), required=False)
    telegram = forms.CharField(label="Телеграм", help_text="<small>Ваш логин в телеграме</small>", max_length=25, widget=forms.TextInput(attrs={'class': 'form-control',}), required=False)

    class Meta:
        model = Profile
        fields = ('about', 'telegram')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите емайл'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}), required=False)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}), required=False)
    
    def is_valid(self):
        logger.info(force_text(self.errors))
        return super(SignUpForm, self).is_valid()

    class Meta:
        model = User
        exclude =('username',)
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        # self.fields['username'].label = ''
        # self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Введите пароль снова'
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = ''