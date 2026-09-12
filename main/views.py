from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book, Comment
from .forms import BookForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
    comments = Comment.objects.filter(book_id=book_id).order_by('-created')
    context = {
        'book':book,
        'comments':comments,
        'title': book.title,
        'form': CommentForm()
    }
    return render(request, 'main/book_detail.html', context)

@login_required(login_url='login')
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

@login_required(login_url='all_books')
def save_comment(request, book_id):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            book = get_object_or_404(Book,pk=book_id,published=True)
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            messages.success(request, "Comentariya qo'shildi")
        return redirect('book_detail', book_id=book_id)

    return redirect('all_books')

@require_POST
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)

    except Comment.DoesNotExist:

        return JsonResponse(
            {
                "error": "Comment topilmadi!"
            },
            status=404
        )

    try:

        data = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "Noto'g'ri ma'lumot!"
            },
            status=400
        )

    text = data.get("text", "").strip()

    if not text:
        return JsonResponse(
            {
                "error": "Comment bo'sh bo'lishi mumkin emas!"
            },
            status=400
        )

    comment.text = text
    comment.save()

    return JsonResponse(
        {
            "success": True,
            "text": comment.text
        }
    )


@login_required(login_url='all_books')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        book_id = comment.book.id
        if request.method == 'POST':
            comment.delete()
            return redirect('book_detail', book_id=book_id)
        else:
            return render(request, "main/confirm_delete.html", context={'comment': comment})
    else:
        print('login qiling')
        return redirect('home')




