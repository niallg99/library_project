"""
URL configuration for library_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from library_app.views import AuthorViewSet, ReaderViewSet, BookViewSet, LoanViewSet, book_list_view, create_loan, reader_detail_view

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'readers', ReaderViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('books/', book_list_view, name='book-list'),
    path('api/create_loan/', create_loan, name='create_loan'),
    path('readers/<int:reader_id>/', reader_detail_view, name='reader_detail'),
]
