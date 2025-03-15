from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model"""

    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, data):
        """Ensure the publication year is not in the future."""

        if data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError("This year is on the future!")
        return data

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model.  
    - Includes a nested representation of the author's books.  
    - Uses the BookSerializer to serialize related books.  
    """
    
    books = BookSerializer(many=True, required=False)

    class Meta:
        model = Author
        fields = ['name', 'books']