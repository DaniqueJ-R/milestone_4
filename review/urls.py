from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:book_id>/', views.add_review, name='add_review'),
    path('delete/<int:id>/', views.delete_review, name='delete_review'),
]
