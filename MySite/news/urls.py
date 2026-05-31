from django.urls import path
from django.views.decorators.cache import cache_page
from . import views
from .views import NewsByCategory, ViewsNews, CreateNews, DeleteNews

urlpatterns = [
    path('', views.home, name='home'),
    # Форма обратной связи (общее задание)
    path('contact/', views.contact, name='contact'),
    # Капча-пазл (индивидуальное задание)
    path('contact/puzzle/', views.contact_puzzle, name='contact_puzzle'),
    # Старая тестовая страница
    path('test/', views.test, name='test'),
    path('category/<int:category_id>', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewsNews.as_view(), name='view_news'),
    path('news/add-news', CreateNews.as_view(), name='add_news'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
]

# ─── cache_page для главной страницы (общее задание, закомментировать при разработке)
# urlpatterns[0] = path('', cache_page(60)(views.home), name='home')
