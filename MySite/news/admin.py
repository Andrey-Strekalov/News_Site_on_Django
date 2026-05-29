from django.contrib import admin
from .models import News, Category, Comment


# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', "category", 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title', 'content', 'category')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'news', 'created_at')
    list_display_links = ('id', 'author')

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
