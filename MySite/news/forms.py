from django import forms
from .models import Category, News

import re
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

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


# ─── Форма обратной связи (общее задание) ─────────────────────────────────────
class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    content = forms.CharField(
        label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )
    # Индивидуальное (вариант 11): серый фон задаётся через CAPTCHA_BACKGROUND_COLOR
    captcha = CaptchaField()


# ─── Форма с капчей-пазлом (индивидуальное задание, вариант 11) ───────────────
class PuzzleCaptchaField(forms.Field):
    """Капча-пазл: пользователь выбирает правильный фрагмент из 4 вариантов.
    Правильный индекс хранится в сессии под ключом 'puzzle_answer'.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Пазл-капча')
        super().__init__(*args, **kwargs)
        self.widget = forms.RadioSelect()

    def validate(self, value):
        super().validate(value)

    def to_python(self, value):
        if value in (None, ''):
            raise ValidationError('Выберите правильный фрагмент.')
        return value


class ContactFormPuzzle(forms.Form):
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    content = forms.CharField(
        label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )
    puzzle_answer = forms.ChoiceField(
        label='Какой фрагмент стоит на месте знака вопроса?',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=[],
    )

    def __init__(self, *args, puzzle_correct=None, puzzle_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._puzzle_correct = puzzle_correct
        if puzzle_choices:
            self.fields['puzzle_answer'].choices = [
                (str(i), label) for i, label in enumerate(puzzle_choices)
            ]

    def clean_puzzle_answer(self):
        value = self.cleaned_data.get('puzzle_answer')
        if self._puzzle_correct is not None and value != str(self._puzzle_correct):
            raise ValidationError('Неверный ответ. Попробуйте ещё раз.')
        return value