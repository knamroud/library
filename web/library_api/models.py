from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth = models.DateField()
    death = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name="books")
    isbn = models.CharField(max_length=200)
    year = models.IntegerField()
    availability = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(
        upload_to="covers", width_field=1600, height_field=2560, null=True, blank=True)
    price = models.DecimalField(default=5.0, max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {' & '.join([author for author in self.authors.all()])}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    date_due = models.DateField()
    date_returned = models.DateField(null=True, blank=True)
    fine = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.borrower.first_name} {self.borrower.last_name} - {self.book}"
