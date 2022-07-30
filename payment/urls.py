from django.urls import path

from payment import views

urlpatterns = [
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('paypal/', views.paypalPaymentMethod, name='paypal_payment'),
]
