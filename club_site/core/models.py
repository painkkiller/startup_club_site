from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

PROJECT_STATUS_CHOICES = (
    ('Идея', 'Идея'),
    ('Разработка прототипа', 'Разработка прототипа'),
    ('Маштабирование', 'Маштабирование'),
)

VACANCY_TYPE_CHOICES = (
    ('Доля в проекте', 'Доля в проекте'),
    ('Зарплата', 'Зарплата'),
    ('Сдельная оплата', 'Сдельная оплата'),
)

SPECIALTIES_TYPES = (
    ('Программист', 'Программист'),
    ('Маркетолог', 'Маркетолог'),
    ('Менеджер', 'Менеджер'),
    ('Дизайнер', 'Дизайнер'),
)

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=False, default='new', unique=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    founders = models.ManyToManyField(User)
    status = models.CharField(max_length=25, choices=PROJECT_STATUS_CHOICES, default='Идея')
    site = models.URLField(max_length=255, null=True)
    preza = models.FileField(upload_to='projects/%Y/%m/', blank=True)
    video_pitch = models.URLField(max_length=255, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    

    class Meta:
        ordering = ('-publish',)

        def __str__(self):
            return self.title


class Vacancy(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacancies')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='vacancies')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    specialty = models.CharField(max_length=25, choices=SPECIALTIES_TYPES, default='Менеджер')
    vacancy_type = models.CharField(max_length=25, choices=VACANCY_TYPE_CHOICES, default='Зарплата')

    class Meta:
        ordering = ('-created',)

        def __str__(self):
            return self.title
