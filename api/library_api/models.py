from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth = models.DateField()
    death = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    isbn = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} - {self.author}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_borrowed = models.DateField()
    date_due = models.DateField()

    def __str__(self):
        return f"{self.borrower.first_name} {self.borrower.last_name} - {self.book.title}"
