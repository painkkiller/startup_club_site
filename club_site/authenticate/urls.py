from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

   path('login', views.login_user, name="login_user"),
   path('logout', views.logout_user, name="logout_user"),
   path('register', views.register_user, name='register'),
   path('users/', views.get_users, name='get_users'),
   path('users/<int:id>/edit', views.edit_profile, name='edit_user'),
   path('users/<int:id>/', views.get_user, name='get_user'),
   re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_user, name='activate'),
]