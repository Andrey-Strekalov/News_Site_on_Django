from django.shortcuts import render
from django.http import HttpResponse

from  .models import News

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
        'title': 'Список новостей'
    }
    return render(request, 'news/index.html', context)




def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>'
                        '<p>Тестовый абзац</p>')

def test2(request):
    return HttpResponse('<h1 style="font-size: 100px">Тестовая страница 2</h1>')


