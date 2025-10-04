from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.


class Donation(models.Model):
    payment_number = models.CharField(max_length=32, null=False, editable=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')


    def _generate_payment_number(self):
        """
        Generate a random, unique payment number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the payment number
        if it hasn't been set already.
        """
        if not self.payment_number:
            self.payment_number = self._generate_payment_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation {self.payment_number} - {self.full_name}"
