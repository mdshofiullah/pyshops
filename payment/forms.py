from django import forms
from payment.models import BillingAddress
from order.models import Order


class BillingAddressFrom(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = [
            'user',
            'first_name',
            'last_name',
            'county',
            'address1',
            'address2',
            'city',
            'zipcode',
            'phone_number',
        ]


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', ]
