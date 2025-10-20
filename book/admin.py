from django.contrib import admin
from .models import Book, TrackerList, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'book_id',
        'title',
        'author',
        'updated_on',
    )

    ordering = ('book_id',)

    search_fields = ['title', 'author']
    list_filter = ['genre']


class TrackerListAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'added_on']
    list_filter = ['status']


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(TrackerList, TrackerListAdmin)
