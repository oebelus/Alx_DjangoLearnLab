from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import render
from .models import Library
from .models import Book

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        
        context['libraries'] = Book.objects.filter(libraries=library)
        print(context)
        return context
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "login.html"

class CustomLogoutView(LogoutView):
    template_name = "logout.html"

def index(request):
    return render(request, "index.html")

def is_admin(user):
    return user.userprofile == 'Admin'

def is_librarian(user):
    return user.userprofile == 'Librarian'

def is_member(user):
    return user.userprofile == 'Member'

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required("relationship_app.can_add_book")
def can_add_book_view(request):
    return render(request, 'relationship_app/can_add_book.html')

@permission_required("relationship_app.can_change_book")
def can_change_book_view(request):
    return render(request, 'relationship_app/can_change_book.html')

@permission_required("relationship_app.can_delete_book")
def can_delete_book_view(request):
    return render(request, 'relationship_app/can_delete_book.html')