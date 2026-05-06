from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from  .models import News, Category

# Create your views here.

# def index (request):
#     news = News.objects.all()
#     res = '<h1>Список новостей</h1>'
#     for item in news:
#         res+=f'<div>\n<p>{item.title}</p>\n<p>{item.content}</p>\n</div>\n<hr>'
#     return HttpResponse(res)



def index(request):
    news = News.objects.all()
    context={
        'news':news,
        'title': 'Список новостей',

    }
    return render(request, 'news/index.html', context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {
        'news': news,
        'category': category
    })

def view_news(request, news_id):
    # news = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})

def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>'
                        '<p>Тестовый абзац</p>')

def test2(request):
    return HttpResponse('<h1 style="font-size: 100px">Тестовая страница 2</h1>')


