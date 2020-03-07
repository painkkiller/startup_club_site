from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import SignUpForm, EditProfileForm



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('you logged in'))
            return redirect('home')
        else:
            messages.success(request, ('error log in'))
            return redirect('login_user')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    # Redirect to a success page.
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('form', form.errors)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('you logged in'))
            return redirect('home')
    else:
        form = SignUpForm()
    context = { 'form': form }
    return render(request, 'register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.user)
        print('form', form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, ('you edited profile'))
            return redirect('home')
    else:
        form = EditProfileForm()
    context = { 'form': form }
    return render(request, 'register.html', context)