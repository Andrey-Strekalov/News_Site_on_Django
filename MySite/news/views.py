from django.db.models import F, Count
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import News, Category
from .forms import NewsForm
from .utils import MyMixin, RelatedObjectsCountMixin


def home(request):
    news = (News.objects
            .filter(is_published=True)
            .select_related('category')
            .annotate(comments_count=Count('comments')))
    paginator = Paginator(news, 5)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, 'news/home_news_list.html', {
        'news': page_obj,
        'page_obj': page_obj,
        'title': 'Главная страница',
    })


def test(request):
    objects = ["john1", "paul2", "george3", "ringo4", "john5", "paul6", "george7"]
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class ViewsNews(DetailView):
    model = News
    context_object_name = 'news_item'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        News.objects.filter(pk=kwargs['pk']).update(views=F('views') + 1)
        return response


class NewsByCategory(RelatedObjectsCountMixin, MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            category_id=self.kwargs['category_id'], is_published=True
        )


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')
    raise_exception = True


class DeleteNews(DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('home')
