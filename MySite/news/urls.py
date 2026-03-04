from django.urls import path
from . import views  # Импортируем views из текущего каталога
from .views import get_category

urlpatterns = [
    path('', views.index, name='home'),
    path('/category/<int:category_id>/', get_category,  name='category'),
#   path('test/', views.test, name='test'),
#   path('test2/', views.test2, name='test2'),


]