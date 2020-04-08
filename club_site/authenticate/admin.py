from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms

from django.contrib.auth import get_user_model
from .models import Profile
from .forms import SignUpForm

User = get_user_model()

class SignUpAdminForm(SignUpForm):
      def __init__(self, *args, **kwargs):
        super(SignUpAdminForm, self).__init__(*args, **kwargs)
        self.fields['termsofuse'].required = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    verbose_name = "Профиль"
    readonly_fields = ["user"]
    search_fields = ('user',)

    def __str__(self):
        return self.user

class CustomUserAdmin(UserAdmin):
    add_form = SignUpAdminForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
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
    #inlines = (UserInline, )

    def save_model(self, request, obj, form, change):
        print('save_model user', request.POST, obj, form, change)
        super().save_model(request, obj, form, change)



admin.site.register(User, CustomUserAdmin)
#admin.site.register(Profile)

admin.site.unregister(Group)
