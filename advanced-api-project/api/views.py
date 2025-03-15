from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from .serializers import AuthorSerializer, BookSerializer
from django_filters import rest_framework
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from .models import Book, Author

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = self.queryset

        name_filter = self.request.query_params.get('name', None)
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = self.queryset

        author_name = self.request.query_params.get('author', None)
        if author_name is not None:
            queryset = queryset.filter(name__icontains=author_name)
        return queryset
    
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']  # Allow filtering by author
    search_fields = ['title', 'author']  # Allow search by book title and author
    ordering_fields = ['publication_year']

class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author", "publication_year"]

    permission_classes = [IsAuthenticatedOrReadOnly]

class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CreateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
class UpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]