from django.urls import path
from . import views

urlpatterns = [
    path('success/<str:payment_number>/', views.payment_success, name="success"),
    path('donations/', views.make_payment, name="donations"),
]

# path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),
