from django.contrib import admin
from .models import Post
from star_ratings import get_star_ratings_rating_model

Rating = get_star_ratings_rating_model()

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


#admin.site.unregister(Rating)