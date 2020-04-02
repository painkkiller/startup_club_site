from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms

from django.contrib.auth import get_user_model
from .models import Profile
from .forms import SignUpForm

User = get_user_model()



class UserInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name = Profile

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name' 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserInline, )



admin.site.register(User, CustomUserAdmin)
