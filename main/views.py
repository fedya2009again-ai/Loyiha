from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book, Comment
from .forms import BookForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, published=True)
    comment = Comment.objects.filter(book_id=book_id).order_by('-created')
    context = {
        'book':book,
        'comment':comment,
        'title': book.title
    }
    return render(request, 'main/book_detail.html', context)

@login_required(login_url='all_books')
def create_book(request):
    if request.method == "POST":
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, "Kitob muvaffaqiyatli qo'shildi")
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm()
    context = {
        'form':form,
        'title': "Kitob qo'shish"
    }
    return render(request, 'main/book-form.html', context)

@login_required(login_url='all_books')
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(data=request.POST,files=request.FILES,instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    context = {
        'form': form,
        'book': book,
        'title': "O'zgartirilmoqda: " + book.title
    }
    return render(request, 'main/book-form.html', context)


@login_required(login_url='all_books')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Kitob muvaffaqiyatli o'chirildi")
        return redirect('all_books')

    context = {
        'book': book
    }

    return render(request, 'main/book_confirm_delete.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')





