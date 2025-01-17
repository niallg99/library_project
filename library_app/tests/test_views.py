from django.test import TestCase
from django.urls import reverse
from library_app.models import Reader, Book, Loan

class ViewTest(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(
            first_name='Bob',
            last_name='Builder',
            email='bob.builder@example.com'
        )
        self.book = Book.objects.create(title='View Book', isbn='8888888888888')

    def test_book_list_view(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_app/book_list.html')

    def test_create_loan_api(self):
        url = reverse('create_loan')
        data = {'book_id': self.book.id, 'reader_id': self.reader.id}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Loan.objects.count(), 1)
        loan = Loan.objects.first()
        self.assertEqual(loan.book, self.book)
        self.assertEqual(loan.reader, self.reader)