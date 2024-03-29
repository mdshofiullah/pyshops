from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect

# models
from django.urls import reverse

from payment.models import BillingAddress
from payment.forms import BillingAddressFrom, PaymentMethodForm
from order.models import Cart, Order

from django.conf import settings
import json
# view
from django.views.generic import TemplateView

# from sslcommerz_python.payment import SSLCSession
# from decimal import Decimal
#
# from django.views.decorators.csrf import csrf_exempt


class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        save_address = BillingAddress.objects.get_or_create(user=request.user or None)
        save_address = save_address[0]
        form = BillingAddressFrom(instance=save_address)
        payment_method = PaymentMethodForm()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].orderItems.all()
        order_total = order_qs[0].get_totals()

        pay_meth = request.GET.get('pay_meth')
        context = {
            'billing_address': form,
            'order_item': order_item,
            'order_total': order_total,
            'payment_method': payment_method,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
            'pay_meth': pay_meth,
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request, *args, **kwargs):
        save_address = BillingAddress.objects.get_or_create(user=request.user or None)
        save_address = save_address[0]
        form = BillingAddressFrom(instance=save_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressFrom(request.POST, instance=save_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()

                if not save_address.is_fully_filled():
                    return redirect('checkout')

                # Cash on delivery process
                if pay_method.payment_method == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print('Order Submitted successfully')
                    return redirect('store:index')

                # Paypal payment process
                if pay_method.payment_method == 'PayPal':
                    return redirect(reverse('checkout') + "?pay_meth=" + str(pay_method.payment_method))

                # sslcommerze payment process
#                 if pay_method.payment_method == 'SSLcomerz':
#                     store_id = settings.STORE_ID
#                     store_pass = settings.STORE_PASS
#
#                     mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
#                                             sslc_store_pass=store_pass)
#
#                     status_url = request.build_absolute_uri(reverse('status'))
#                     mypayment.set_urls(success_url=status_url, fail_url=status_url,
#                                        cancel_url=status_url, ipn_url=status_url)
#
#                     order_qs = Order.objects.filter(user=request.user, ordered=False)
#                     order_items = order_qs[0].orderitems.all()
#                     order_item_count = order_qs[0].orderitems.count()
#                     order_total = order_qs[0].get_totals()
#                     mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT',
#                                                       product_category='clothing', product_name=order_items,
#                                                       num_of_item=order_item_count, shipping_method='Courier',
#                                                       product_profile='None')
#                     current_user = request.user
#
#                     mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email,
#                                                 address1=current_user.profile.address,
#                                                 address2=current_user.profile.address, city=current_user.profile.city,
#                                                 postcode=current_user.profile.zipcode,
#                                                 country=current_user.profile.country, phone=current_user.profile.phone)
#
#                     billing_address = BillingAddress.objects.filter(user=request.user)[0]
#                     mypayment.set_shipping_info(shipping_to=billing_address.address1, address=billing_address.address2,
#                                                 city=billing_address.city,
#                                                 postcode=billing_address.zipcode, country=billing_address.country)
#
#                     response_data = mypayment.init_payment()
#                     print("=============")
#                     print(response_data)
#                     print("=============")
#                 return redirect('checkout')
#
#
# @csrf_exempt
# def sslc_status(request):
#     if request.method == 'post' or request.method == 'POST':
#         payment_data = request.POST
#         print(payment_data)
#
#     return render(request, 'status.html')
#
#
# def sslc_complete(request, val_id, tran_id):
#     pass


def paypalPaymentMethod(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    payment_id = data['payment_id']
    status = data['status']

    if status == "COMPLETED":
        if request.user.is_authenticated:
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            order = order_qs[0]
            order.ordered = True
            order.orderId = order_id
            order.paymentId = payment_id
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchased=False)
            for item in cart_items:
                item.purchased = True
                item.save()
    return redirect('store:index')
