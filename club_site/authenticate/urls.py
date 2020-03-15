from django.urls import path, re_path
from . import views

urlpatterns = [
   path('login', views.login_user, name="login_user"),
   path('logout', views.logout_user, name="logout_user"),
   path('register', views.register_user, name='register'),
   path('edit', views.edit_profile, name='edit'),
   re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_user, name='activate'),
]