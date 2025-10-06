
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_page, name="index"),
    path('my-library/', views.my_library, name="my-library"),
    path('book-details/<slug:slug>/', views.book_details, name="book-details"),
]
