from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

from .forms import DonationForm
from .models import Donation

import stripe
import json


# Create your views here.


def make_payment(request):
    """
    Handle donation payments - serves the form on GET,
    creates payment intent and saves donation on POST (AJAX)
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # Handle AJAX request to create payment intent
        try:
            amount = request.POST.get('amount')
            
            if not amount:
                return JsonResponse({'error': 'Amount is required'}, status=400)
            
            amount_int = int(amount)
            stripe_total = amount_int * 100
            
            # Create Stripe payment intent
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
            
            # Save donation record
            form_data = {
                'full_name': request.POST.get('full_name'),
                'email': request.POST.get('email'),
                'phone_number': request.POST.get('phone_number'),
                'amount': amount_int,
            }
            donation_form = DonationForm(form_data)
            
            if donation_form.is_valid():
                donation = donation_form.save()
                
                return JsonResponse({
                    'client_secret': intent.client_secret,
                    'payment_number': donation.payment_number,
                })
            else:
                return JsonResponse({
                    'error': 'Form validation failed', 
                    'details': donation_form.errors
                }, status=400)
                
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': f'Invalid amount: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # GET request - show the donation form
        donation_form = DonationForm()
        
        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')
        
        context = {
            'stripe_public_key': stripe_public_key,
            'client_secret': None,  # Created via AJAX on submit
            'donation_form': donation_form,
        }
        return render(request, 'payment/donations.html', context)


def payment_success(request, payment_number):
    """
    Handle successful payments
    """
    donation = get_object_or_404(Donation, payment_number=payment_number)
    messages.success(request, f'Thank you for your donation! \
        Your payment number is {payment_number}. A confirmation \
        email will be sent to {donation.email}.')

    context = {
        'donation': donation,
    }
    return render(request, 'payment/success.html', context)
