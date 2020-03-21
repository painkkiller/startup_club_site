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


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=False, default='new', unique=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    founders = models.ManyToManyField(User)
    status = models.CharField(max_length=25, choices=PROJECT_STATUS_CHOICES, default='idea')
    site = models.URLField(max_length=255, null=True)

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    class Meta:
        ordering = ('-publish',)

        def __str__(self):
            return self.title
