from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class EditUserForm(UserChangeForm):
    # password =  forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'type': 'hidden',}))
    first_name =  forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))
    last_name =  forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',}))

    class Meta:
        model = User
        #fields = ('first_name', 'last_name')
        exclude = ('username', 'last_login', 'is_superuser', 'user_permissions', 'groups', 
        'password1', 'password2', 'password', 'is_staff', 'is_active', 'date_joined', 'email')

class EditProfileForm(forms.ModelForm):
    about =  forms.CharField(label="Обо мне", help_text="<small>Расскажите о себе и своих компетенциях</small>", max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control',}))
    telegram = forms.CharField(label="Телеграм", help_text="<small>Ваш логин в телеграме</small>", max_length=25, widget=forms.TextInput(attrs={'class': 'form-control',}))

    class Meta:
        model = Profile
        fields = ('about', 'telegram')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    first_name = forms.CharField(label="", help_text="<strong>Enter your First Name</strong>", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<small> usermane </small>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter Password again'
        self.fields['password2'].label = ''