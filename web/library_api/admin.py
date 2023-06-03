from django.contrib import admin
from .models import Author, Book, Loan

admin.site.register([Author, Book, Loan])
