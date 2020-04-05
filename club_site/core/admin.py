from django.contrib import admin
from .models import Post, Project, Vacancy
from social_django.models import Association, Nonce, UserSocialAuth
from star_ratings import get_star_ratings_rating_model
from star_ratings.models import UserRating

Ratings = get_star_ratings_rating_model()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'author', 'publish','status', 'can_comment')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def save_model(self, request, instance, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.author:
            instance.author = user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('created', )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('updated',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('created', 'author')
    search_fields = ('title', 'description')
    ordering = ('updated',)



admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Ratings)
admin.site.unregister(UserRating)

admin.site.site_header = "Администрация стартап клуба"
admin.site.site_title = "Администрация"
admin.site.index_title = "Добро пожаловать в стартап клуб"