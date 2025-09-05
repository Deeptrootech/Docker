from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from app_bookstall.views import BookView, BookCreate, export_books_excel, export_books_pdf, PublisherCreate, AuthorCreate

urlpatterns = [
    path("", BookView.as_view(), name="book-list"),
    path("add_book/", BookCreate.as_view(), name="book-create"),
    path("add_author/", AuthorCreate.as_view(), name="author-create"),
    path("add_publisher/", PublisherCreate.as_view(), name="publisher-create"),

    path("export/books/pdf/", export_books_pdf, name="export_books_pdf"),
    path("export/books/excel/", export_books_excel, name="export_books_excel"),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
