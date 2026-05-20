from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy

from  .models import News, Category
from .forms import NewsForm


class HomeViews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeViews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

class ViewsNews(DetailView):
    model = News
    context_object_name = 'news_item'

class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')

class DeleteNews(DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('home')



