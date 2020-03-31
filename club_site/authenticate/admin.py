from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm, EditUserForm
from .models import User, Profile


class UserInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name = Profile

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = EditUserForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserInline, )



admin.site.register(User, CustomUserAdmin)
