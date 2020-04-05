from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import SignUpForm, EditUserForm, EditProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from core.mailer import mail_to_users

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
        print('register_user', request.POST['phone'])
        if request.POST['phone']:
            redirect('home') # хлипкая защита от ботов
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            password = form.cleaned_data['password1']
            current_site = get_current_site(request)
            mail_subject = 'Активируйте ваш аккаунт в стартап клубе'
            message = render_to_string('emails/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            resp = mail_to_users(mail_subject, html_content=message, txt_content=message, mails=[to_email])
            if resp == 1:
                messages.success(request, ('Проверьте свой почтовый ящик, чтобы активировать аккаунт'))
                return redirect('home')
            else:
                messages.error(request, ('Не удается отправить вам емайл, что то пошло не так'))
    else:
        form = SignUpForm()
    context = { 'form': form }
    return render(request, 'register.html', context)

@login_required
def edit_profile(request, id):
    if request.method == 'POST':
        userForm = EditUserForm(request.POST, request.user)
        profileForm = EditProfileForm(request.POST, request.user)
        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save(commit=False)
            profile = profileForm.save(commit=False)
            user.id = request.user.id
            profile.id = request.user.id
            profile.user = user
            user.save(update_fields=('first_name', 'last_name'))
            profile.save()
            messages.success(request, ('Вы успешно отредактировали свой профиль'))
            return redirect('get_user', id=request.user.id)
    else:
        user = User.objects.get(pk=id)
        userForm = EditUserForm(instance=user)
        profile = Profile.objects.get(user=id)
        profileForm = EditProfileForm(instance=profile)
    context = { 'userForm': userForm, 'profileForm': profileForm }
    return render(request, 'profileedit.html', context)

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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def get_users(request):
    User = get_user_model()
    if request.method == 'GET':
        users = User.objects.filter(is_active=True)
        context = { 'users': users }
        return render(request, 'userslist.html', context)

def get_user(request, id):
    User = get_user_model()
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        profile = Profile.objects.get(user=id)
        can_edit = (request.user.id == id)
        context = { 'p_user': user, 'profile': profile, 'can_edit': can_edit }
        return render(request, 'profile.html', context)

def termsofuse(request):
    return render(request, 'termsofuse.html')
    
