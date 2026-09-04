from django.urls import path
from .views import all_books, books_by_category

urlpatterns = [
    path('', all_books, name='all_books'),
    path('category/<int:category_id>', books_by_category, name='by_category'),
]