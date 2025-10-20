from django.contrib import admin
from review.models import Review

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'star_rating', 'created_on']
    list_filter = ['star_rating']


admin.site.register(Review, ReviewAdmin)
