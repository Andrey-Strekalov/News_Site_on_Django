from django.urls import path
from . import views  # Импортируем views из текущего каталога
from .views import get_category, add_news

urlpatterns = [
    path('', views.index, name='home'),
    path('/category/<int:category_id>/', get_category,  name='category'),
    path('news/<int:news_id>/', views.view_news, name='view_news'),
    path('news/add-news', add_news, name='add_news'),

]