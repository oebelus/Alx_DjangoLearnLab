from django.urls import path
from .views import LibraryDetailView
from .views import list_books

urlpatterns = [
    path('books/', list_books, name='books-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail')
]