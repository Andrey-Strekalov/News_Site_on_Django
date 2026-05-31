from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category, Comment


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('Заголовок должен содержать не менее 5 символов')
        if title[0].isdigit():
            raise ValidationError('Заголовок не должен начинаться с цифры')
        return title


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')
    inlines = [CommentInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('created_at', 'updated_at', 'views')
        return ()


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
