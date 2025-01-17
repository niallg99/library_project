from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Author, Reader, Book, Loan, BookRequest
from .serializers import AuthorSerializer, ReaderSerializer, BookSerializer, LoanSerializer, BookRequestSerializer

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
    book_requests = BookRequest.objects.filter(reader=reader)

    return render(
        request,
        'library_app/reader_detail.html',
        {
            'reader': reader,
            'loans': loans,
            'book_requests': book_requests
        }
    )

def reader_list_view(request):
    readers = Reader.objects.all()
    book_requests = BookRequest.objects.filter(completed=False)
    return render(
        request,
        'library_app/reader_list.html',
        {'readers': readers, 'book_requests': book_requests}
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

@api_view(['POST'])
def request_book(request):
    book_id = request.data.get('book_id')
    reader_id = request.data.get('reader_id')

    book = get_object_or_404(Book, id=book_id)
    reader = get_object_or_404(Reader, id=reader_id)

    if BookRequest.objects.filter(book=book, completed=False).exists():
        return Response({'error': 'Book request already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if Loan.objects.filter(book=book, returned=False).exists():
        return Response({'error': 'Book is already on loan'}, status=status.HTTP_400_BAD_REQUEST)

    book_request = BookRequest.objects.create(book=book, reader=reader)
    return Response(BookRequestSerializer(book_request).data, status=status.HTTP_201_CREATED)
        