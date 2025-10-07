
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_page, name="index"),
    path('book-details/<slug:slug>/', views.book_details, name="book_details"),
    path('my-library/', views.my_library, name="my_library"),
    path("tracker/add/<int:book_id>/", views.add_or_update_tracker, name="add_tracker"),
    path("tracker/edit/<int:tracker_id>/", views.edit_tracker, name="edit_tracker"),
    path("tracker/delete/<int:tracker_id>/", views.delete_tracker, name="delete_tracker"),
]
