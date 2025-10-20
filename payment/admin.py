from django.contrib import admin
from .models import Donation

# Register your models here.


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'full_name', 'email', 'amount', 'date')
    list_filter = ('email', 'date')
    search_fields = ('payment_number', 'email', 'full_name')
