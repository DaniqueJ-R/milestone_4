import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Donation

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        pid = payment_intent['id']

        try:
            donation = Donation.objects.get(stripe_pid=pid)
            donation.status = 'completed'
            donation.save()
        except Donation.DoesNotExist:
            pass

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        pid = payment_intent['id']
        try:
            donation = Donation.objects.get(stripe_pid=pid)
            donation.status = 'failed'
            donation.save()
        except Donation.DoesNotExist:
            pass

    return HttpResponse(status=200)
