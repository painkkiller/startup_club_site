from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .managers import UserManager



class User(AbstractUser):
    """auth/login-related fields"""
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email 
    # Examples:
    # email (if used for login)
    # extra permissions
    # NOTE: before putting something here make sure it wouldn't be better in the profile model
    #class Meta:
        # model = User
        #fields = ['email', 'password', 'first_name', 'last_name']

class Profile(models.Model):
    """profile fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=2000, blank=True)
    telegram = models.CharField(max_length=25, blank=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    vk = models.URLField(max_length=255, null=True, blank=True)
    # Examples:
    # Display Name
    # Bios, descriptions, taglines
    # Theme (light or dark)
    # email (if not used to log in)
    def __str__(self):
        return self.user.__str__()
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


"""receivers to add a Profile for newly created users"""
@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    print('create_user_profile', created, instance.id)
    if created:
        try:
            p = Profile.objects.create(user = instance)
        except Exception as e:
            print('create profile error', e)
    else:
        instance.profile.save()

""" @receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
    print('save_user_profile')
    try:
        instance.profile.save()
    except Exception:
            print('save profile error', Exception)
 """