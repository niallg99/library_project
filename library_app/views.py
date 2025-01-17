from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Author, Reader, Book, Loan
from .serializers import AuthorSerializer, ReaderSerializer, BookSerializer, LoanSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'isbn']

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['book__title', 'reader__first_name', 'reader__last_name']

def book_list_view(request):
    books = Book.objects.all()
    return render(
        request, 
        'library_app/book_list.html', 
        {'books': books}
    )

def reader_detail_view(request, reader_id):
    reader = Reader.objects.get(id=reader_id)
    loans = Loan.objects.filter(reader=reader)
    return render(
        request,
        'library_app/reader_detail.html',
        {
            'reader': reader,
            'loans': loans
        }
    )

def reader_list_view(request):
    readers = Reader.objects.all()
    return render(
        request,
        'library_app/reader_list.html',
        {'readers': readers}
    )

@api_view(['POST'])
def create_loan(request):
    book_id = request.data.get('book_id')
    reader_id = request.data.get('reader_id')
    due_date = request.data.get('due_date')

    try:
        book = Book.objects.get(id=book_id)
        reader = Reader.objects.get(id=reader_id)
        loan = Loan.objects.create(
            book=book,
            reader=reader,
            due_date=due_date
        )
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    except Reader.DoesNotExist:
        return Response({'error': 'Reader not found'}, status=status.HTTP_404_NOT_FOUND)
        