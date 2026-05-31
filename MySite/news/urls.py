from django.urls import path
from . import views
from .views import NewsByCategory, ViewsNews, CreateNews, DeleteNews

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('category/<int:category_id>', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewsNews.as_view(), name='view_news'),
    path('news/add-news', CreateNews.as_view(), name='add_news'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
]
