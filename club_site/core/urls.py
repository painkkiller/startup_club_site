from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('projects/', views.projects, name="projects"),
    path('projects/<slug:slug>/', views.project_details, name="project_details"),
    path('projects/<slug:slug>/edit', views.project_edit, name="project_edit"),
]