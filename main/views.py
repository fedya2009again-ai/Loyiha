from django.shortcuts import render, get_object_or_404
from .models import Category, Book, Comment

def all_books(request):
    categories = Category.objects.all()
    books = Book.objects.filter(published=True)
    context = {
        'categories':categories,
        'books':books,
        'title': "Asosiy sahifa"
    }
    return render(request, 'main/all_books.html', context   )

def books_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category_id=category_id, published=True)
    categories = Category.objects.all()
    context = {
        'books':books,
        'categories':categories,
        'title': category.name
    }
    return render(request, 'main/all_books.html', context)

