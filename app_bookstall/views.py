from django.shortcuts import render
from django.views.generic import ListView, CreateView

import pandas as pd
from django.http import HttpResponse
from app_bookstall.models import Book
from django.template.loader import render_to_string
import pdfkit


# Create your views here.
class BookView(ListView):
    context_object_name = "book"
    model = Book
    template_name = "book_list.html"


class BookCreate(CreateView):
    model = Book
    fields = ["title", "authors", "publisher"]
    template_name = "add_book.html"
    success_url = "/books"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def export_books_excel(request):
    books = Book.objects.all().values("title", "authors__name", "publisher__name")
    df = pd.DataFrame(books)
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="books.xlsx"'
    df.to_excel(response, index=False)
    return response


# Export Books as PDF
def export_books_pdf(request):
    books = Book.objects.all()
    html = render_to_string("admin/app_bookstall/book/books_pdf_template.html", {"books": books})

    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="books.pdf"'
    return response

