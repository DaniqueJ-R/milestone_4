from django.contrib import admin
from .models import Donation

# Register your models here.

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'full_name', 'email', 'amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('payment_number', 'email', 'full_name')
