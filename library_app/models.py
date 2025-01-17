from django.db import models
from django.utils import timezone

"""
Human model to store common fields for Author and Reader models
"""
class Human(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        abstract = True
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Author(Human):
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'

class Reader(Human):
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name}'

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['isbn'], name='isbn_index')  # For faster lookups on ISBN.
        ]

    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.borrowed_at + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book.title} borrowed by {self.reader.full_name} at {self.borrowed_at}'

    @property
    def is_overdue(self):
        if self.returned:
            return False
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False

class BookRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requests')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='requests')
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if Loan.objects.filter(book=self.book, returned=False).exists():
            raise ValidationError('Book is already borrowed')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book.title} requested by {self.reader.full_name}'