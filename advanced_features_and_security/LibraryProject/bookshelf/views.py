from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from pyexpat.errors import messages
from .forms import ExampleForm
from .models import Author
from .models import Book

# Create your views here.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books':books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        publication_year = request.POST.get('publication_year')
        author_id = request.POST.get('author_id')

        author = get_object_or_404(Author, id=author_id)
        book = Book.objects.create(title=title, publication_year=publication_year, author=author)
        messages.success(request, "Book added successfully.")
        return redirect('book_list')
    return render(request, 'bookshelf/add_book.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.publication_year = request.POST.get('publication_year')
        book.author_id = request.POST.get('author_id')

        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('book_list')
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})    

def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})