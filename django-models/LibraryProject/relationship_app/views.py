from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.
def books_view(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'list_books.html', context)

class LibraryView(DetailView):
    model = Library
    template_name = 'list_library.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        
        context['libraries'] = Book.objects.filter(libraries=library)
        print(context)
        return context