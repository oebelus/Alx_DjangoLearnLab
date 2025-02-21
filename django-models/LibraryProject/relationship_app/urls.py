from django.urls import path
from .views import LibraryView, books_view

urlpatterns = [
    path('books/', books_view, name='books-list'),
    path('library/<int:pk>/', LibraryView.as_view(), name='library-detail')
]