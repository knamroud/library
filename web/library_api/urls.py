from django.urls import path
from . import views

urlpatterns = [
    path("books", views.BookView.as_view()),
    path("books/<int:pk>", views.BookDetailView.as_view()),
    path("authors", views.AuthorView.as_view()),
    path("authors/<int:pk>", views.AuthorDetailView.as_view()),
    path("loans", views.LoanView.as_view()),
    path("loans/<int:pk>", views.LoanDetailView.as_view()),
]
