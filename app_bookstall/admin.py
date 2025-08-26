from django.contrib import admin
from django.http import HttpResponse

from app_bookstall.models import Publisher, Author, Book

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Author)


class BookAdmin(admin.ModelAdmin):
    change_list_template = "admin/app_bookstall/book/change_list.html"  # Custom template for list view


admin.site.register(Book, BookAdmin)
