# import stripe
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from .models import Donation

# stripe.api_key = settings.STRIPE_SECRET_KEY

# @require_POST
# @csrf_exempt
# def webhook(request):
#     """Listen for webhooks from Stripe"""
#     # Setup
#     wh_secret = settings.STRIPE_WH_SECRET
#     stripe.api_key = settings.STRIPE_SECRET_KEY

#     # get the webhook data and verify its signature
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, wh_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
    
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
    
#     except Exception as e:
#         return HttpResponse(content=e, status=400)



#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']
#         pid = payment_intent['id']

#         try:
#             donation = Donation.objects.get(stripe_pid=pid)
#             donation.status = 'completed'
#             donation.save()
#         except Donation.DoesNotExist:
#             pass

#     elif event['type'] == 'payment_intent.payment_failed':
#         payment_intent = event['data']['object']
#         pid = payment_intent['id']
#         try:
#             donation = Donation.objects.get(stripe_pid=pid)
#             donation.status = 'failed'
#             donation.save()
#         except Donation.DoesNotExist:
#             pass

#     return HttpResponse(status=200)


# # from tutorial
# from django.http import HttpResponse
# from django.conf import settings
# from django.views.decorators.http import require_POST
# from django.views.decorators.csrf import csrf_exempt

# from checkout.webhook_handler import StripeWH_Handler

# import stripe

# # from tutorial
# @require_POST
# @csrf_exempt
# def webhook(request):
#     """Listen for webhooks from Stripe"""
#     # Setup
#     wh_secret = settings.STRIPE_WH_SECRET
#     stripe.api_key = settings.STRIPE_SECRET_KEY

#     # get the webhook data and verify its signature
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WH_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
    
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
    
#     except Exception as e:
#         return HttpResponse(content=e, status=400)
    
#     # Set up a webhook handler
#     handler = StripeWH_Handler(request)

#     # Map webhook events to relevant handler functions
#     event_map = {
#         'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
#         'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
#     }

#     # Get the webhook type from Stripe
#     event_type = event['type']

#     # If there's a handler for it, get it from the event map
#     # Use the generic one by default
#     event_handler = event_map.get(event_type, handler.handle_event)
    
#     # Call the event handler with the event
#     response = event_handler(event)
#     return response


# #  from GPT

# import stripe
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from .models import Donation

# stripe.api_key = settings.STRIPE_SECRET_KEY

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except (ValueError, stripe.error.SignatureVerificationError):
#         return HttpResponse(status=400)

#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']
#         pid = payment_intent['id']

#         try:
#             donation = Donation.objects.get(stripe_pid=pid)
#             donation.status = 'completed'
#             donation.save()
#         except Donation.DoesNotExist:
#             pass

#     elif event['type'] == 'payment_intent.payment_failed':
#         payment_intent = event['data']['object']
#         pid = payment_intent['id']
#         try:
#             donation = Donation.objects.get(stripe_pid=pid)
#             donation.status = 'failed'
#             donation.save()
#         except Donation.DoesNotExist:
#             pass

#     return HttpResponse(status=200)
