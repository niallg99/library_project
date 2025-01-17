from django.contrib import admin
from .models import Author, Reader, Book, Loan, BookRequest

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'membership_date')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'published_date')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'borrowed_at', 'due_date', 'returned', 'is_overdue')

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'completed',)
    list_filter = ('completed',)
