from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('donations/', views.make_payment, name="donations"),
    path('wh/', webhook, name='webhook'),
    path('success/<str:payment_number>/', views.payment_success, name="success"),
]
