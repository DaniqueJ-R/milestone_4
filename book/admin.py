from django.contrib import admin
from .models import Book, TrackerList, Genre
from review.models import Review

class BookAdmin(admin.ModelAdmin):
    list_display = (
        'book_id',
        'title',
        'author',
        # 'genre',
        'updated_on',
    )

    ordering = ('book_id',)

    search_fields = ['title', 'author']
    # list_filter = ['genre']

class UserBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'date_added']
    list_filter = ['status']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'star_rating', 'created_on']
    list_filter = ['star_rating']

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
admin.site.register(TrackerList)
