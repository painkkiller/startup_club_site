from django.urls import path
from . import views

urlpatterns = [
   path('login', views.login_user, name="login_user"),
   path('logout', views.logout_user, name="logout_user"),
   path('register', views.register_user, name='register'),
   path('edit', views.edit_profile, name='edit'),
]