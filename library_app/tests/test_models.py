from django.test import TestCase
from library_app.models import Author, Reader, Book, Loan

class ModelTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com'
        )
        self.assertEqual(str(author), 'Jane Doe')

    def test_create_reader(self):
        reader = Reader.objects.create(
            first_name='Alice',
            last_name='Wonderland',
            email='alice@example.com'
        )
        self.assertEqual(str(reader), 'Alice Wonderland')

    def test_create_book(self):
        author = Author.objects.create(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com'
        )
        book = Book.objects.create(title='Test Book', isbn='1234567890123')
        book.authors.add(author)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertIn(author, book.authors.all())
        self.assertEqual(str(book), 'Test Book')

    def test_create_loan(self):
        reader = Reader.objects.create(
            first_name='Alice',
            last_name='Wonderland',
            email='alice@example.com'
        )
        book = Book.objects.create(title='Another Book', isbn='9999999999999')
        loan = Loan.objects.create(book=book, reader=reader)
        self.assertFalse(loan.returned)
        self.assertEqual(str(loan), 'Another Book borrowed by Alice Wonderland')