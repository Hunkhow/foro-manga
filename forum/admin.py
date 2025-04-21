from django.contrib import admin
from .models import Genre, Tag, Manga, Thread, Post, Upvote

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display        = ('title', 'get_genres', 'get_tags', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter         = ('genres','tags')
    filter_horizontal   = ('genres','tags')
    search_fields       = ('title','description')

    def get_genres(self, obj):
        # Une todos los nombres de géneros en una cadena separada por comas
        return ", ".join(obj.genres.values_list('name', flat=True))
    get_genres.short_description = 'Géneros'

    def get_tags(self, obj):
        # Une todos los nombres de tags en una cadena separada por comas
        return ", ".join(obj.tags.values_list('name', flat=True))
    get_tags.short_description = 'Tags'



@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'manga', 'is_closed', 'views', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('manga', 'is_closed', 'tags')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    list_filter = ('thread',)

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('user',)