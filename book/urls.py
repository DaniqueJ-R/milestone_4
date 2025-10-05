
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_page, name="index"),
    # path('my_library/', views.my_library, name="my_library"),
    path('book-details/<slug:slug>/', views.book_details, name="book-details"),
]
