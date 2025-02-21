from django.contrib.auth.views import LoginView, LogoutView
from .views import LibraryDetailView
from .views import list_books
from .views import index
from django.urls import path
from . import views

urlpatterns = [
    path('books/', list_books, name='books-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("", index, name="index")
]