from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import SignUpForm, EditProfileForm
from .models import Profile
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

User = get_user_model()



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
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # user = authenticate(request, username=username, password=password)
            # login(request, user)
            current_site = get_current_site(request)
            mail_subject = 'Активируйте ваш аккаунт в стартап клубе'
            # print('register_user.pk = ', user.pk, 'uid = ', force_text(urlsafe_base64_encode(force_bytes(user.pk))))
            message = render_to_string('emails/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            sender = "postmaster@startup-club.tech"
            email = EmailMultiAlternatives(
                        mail_subject, message, sender, [to_email]
            )
            resp = email.send()
            if resp == 1:
                messages.success(request, ('Проверьте свой почтовый ящик, чтобы активировать аккаунт'))
                return redirect('home')
            else:
                messages.error(request, ('Не удается отправить вам емайл, что то пошло не так'))
    else:
        form = SignUpForm()
    context = { 'form': form }
    return render(request, 'register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('you edited profile'))
            return redirect('home')
    else:
        form = EditProfileForm()
    context = { 'form': form }
    return render(request, 'register.html', context)

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def get_users(request):
    User = get_user_model()
    if request.method == 'GET':
        users = User.objects.all()
        context = { 'users': users }
        return render(request, 'userslist.html', context)

def get_user(request, id):
    print('get_user', id)
    User = get_user_model()
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        profile = Profile.objects.get(user=id)
        print('get_user 2', user, profile)
        context = { 'user': user, 'profile': profile }
        return render(request, 'profile.html', context)
    
