from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('comments/', include('django_comments.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('projects/', views.projects, name="projects"),
    path('projects/<slug:slug>/', views.project_details, name="project_details"),
    path('projects/<slug:slug>/edit', views.project_edit, name="project_edit"),
    path('vacancies/', views.vacancies, name="vacancies"),
    path('vacancies/<int:id>/', views.vacancy_details, name="vacancy_details"),
    path('vacancies/<int:id>/edit', views.vacancy_edit, name="vacancy_edit"),
    path('vacancies/<int:id>/delete', views.vacancy_delete, name="vacancy_delete"),
    path('contacts/', views.contacts, name="contacts"),
    path('useful/', views.useful, name="useful"),
    path('<str:post_type>/<slug:slug>/', views.post_details, name="post_details"),
    path('news/', views.news, name="news"),
]