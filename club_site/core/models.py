from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django_comments.models import Comment
from django_comments.signals import comment_was_posted
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from .mailer import mail_to_users

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

TYPE_CHOICES = (
    ('index', 'index'),
    ('useful', 'useful'),
    ('news', 'news'),
)

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
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
    ratings = GenericRelation(Rating, related_query_name='projects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_details', kwargs={'slug': self.slug })



""" class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author =  models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {}'.format(self.body) """

class Post(models.Model):
    title = models.CharField(max_length=250)
    post_type = models.CharField(max_length=25, choices=TYPE_CHOICES, default='news')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    can_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        print('get_absolute_url', self.slug, self.post_type)
        return reverse('post_details', kwargs={'slug': self.slug, 'post_type': self.post_type })

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


@receiver(comment_was_posted, sender=Comment)
def notify_about_comment(sender, **kwargs):
    comment = kwargs.get('comment')
    project = Project.objects.get(pk=comment.content_object.id)
    subject_mail = 'Ваш проект прокомментировали'
    emails = [founder.email for founder in project.founders.all()]
    current_site = get_current_site(kwargs.get('request'))
    html_message = render_to_string('emails/commentedproject.html', {
        'domain': current_site.domain,
        'project': project,
        'comment': comment, 
    })
    txt_message = render_to_string('emails/commentedproject.txt', {
        'domain': current_site.domain,
        'project': project,
        'comment': comment,
    })
    mail_to_users(subject_mail, html_message, txt_message, emails)   