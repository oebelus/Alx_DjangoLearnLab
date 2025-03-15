from .views import CreateView, DeleteView, ListView, DetailView, UpdateView
from django.urls import path

urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-details'),
    path('books/create/', CreateView.as_view(), name='add-book'),
    path('books/update/<int:pk>/', UpdateView.as_view(), name='update-book'),
    path('books/delete/<int:pk>', DeleteView.as_view(), name='delete-book'),
]