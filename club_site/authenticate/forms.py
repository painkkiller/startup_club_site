from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class EditProfileForm(UserChangeForm):
    password =  forms.CharField(label="", help_text="<strong>Enter your First Name</strong>", max_length=100, widget=forms.TextInput(attrs={'type': 'hidden',}))
    class Meta:
        model = User
        exclude = ('username', 'last_login', 'is_superuser', 'user_permissions', 'groups', 
        'password1', 'password2', 'is_staff', 'is_active', 'date_joined')


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