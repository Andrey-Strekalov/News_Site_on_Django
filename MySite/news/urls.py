from django.urls import path
from . import views  # Импортируем views из текущего каталога
from .views import   HomeViews, NewsByCategory, ViewsNews, CreateNews, DeleteNews

urlpatterns = [
    path('', HomeViews.as_view(), name='home'),
    path('category/<int:category_id>', NewsByCategory.as_view(extra_context={'title': 'Какой-то заголовок'}),
         name='category'),
    path('news/<int:pk>/', ViewsNews.as_view(), name='view_news'),
    path('news/add-news', CreateNews.as_view(), name='add_news'),
path('news/<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
]