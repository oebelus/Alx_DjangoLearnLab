from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import BookSerializer
from rest_framework import status
from rest_framework import views
from .models import Book

class ListView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class DetailView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_book_by_id(self, id, request):
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class CreateView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def add_book(self, book_data):
        book = Book.object.create(
            title=book_data['title'],
            publication_year=book_data['publication_year'],
            author=book_data['author']
        )

        return book
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            book = self.add_book(serializer.validated_data)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update_book(self, book, book_data):
        book.title = book_data['title']
        book.publication_year = book_data['publication_year']
        book.author = book_data['author']
        book.save()

        return book

    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            self.update_book(book, serializer.validated_data)
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

class DeleteView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, id, request):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        
        book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)