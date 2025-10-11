


from django.urls import path
from . import views

urlpatterns = [
    path('success/', views.payment_sucess, name="success"),
]    

# path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),


# ⚡ 4. Is it a lot of work?

# Not really ✅ —

# Setting up the webhook view = 15–20 lines of code (like above).

# You just need to add your STRIPE_WEBHOOK_SECRET from Stripe Dashboard to your Heroku config vars.

# Stripe will call that URL automatically whenever a payment changes state.

# Once it’s set up, your donation records stay in sync with Stripe automatically.