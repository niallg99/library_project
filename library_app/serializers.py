from rest_framework import serializers
from .models import Author, Reader, Book, Loan

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = (
            'first_name',
            'last_name',
            "full_name",
            'date_of_birth',
            'email',
            'bio',
        )

    def get_full_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = (
            'first_name',
            'last_name',
            "full_name",
            'date_of_birth',
            'email',
            'membership_date',
        )
    
    def get_full_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'isbn',
            'published_date',
            'summary',
        )


class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    reader = ReaderSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = (
            'book',
            'reader',
            'borrowed_at',
            'due_date',
            'returned',
        )