from django import forms
from .models import Category, News

import re
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            'category': forms.Select(attrs={"class": "form-control"}),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

    def clean(self):
        cleaned_data = super().clean()
        is_published = cleaned_data.get('is_published')
        content = cleaned_data.get('content')

        if is_published and not content:
            self.add_error('content', 'Для опубликованной новости необходимо заполнить текст.')
        return cleaned_data