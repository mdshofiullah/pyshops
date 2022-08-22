from django.shortcuts import render, redirect
from django.http import HttpResponse

from account.forms import RegistrationForm, ProfileForm

# Authentication function
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from order.models import Cart, Order
from payment.models import BillingAddress
from payment.forms import BillingAddressFrom
from account.models import Profile

from django.views.generic import TemplateView


def register(request):
    if request.user.is_authenticated:
        return HttpResponse('you are registered and have to redirect to shop page')
    else:
        form = RegistrationForm
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Your Account created successfully')

        context = {
            'form': form
        }
    return render(request, 'register.html', context)


def Customerlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('Your just logged in')
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username=username, password=password)
            if customer is not None:
                login(request, customer)
                return HttpResponse('you logged in successfully!')
            else:
                return HttpResponse('404')

    return render(request, 'login.html')


# Customer Profile

class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, ordered=True)
        billingaddress = BillingAddress.objects.get(user=request.user)
        billingaddress_form = BillingAddressFrom(instance=billingaddress)
        profile_obj = Profile.objects.get(user=request.user)
        profileForm = ProfileForm(instance=profile_obj)
        context = {
            'orders': orders,
            'billingaddress': billingaddress_form,
            'profileForm': profileForm,
        }

        return render(request, 'profile.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'post' or request.method == 'POST':
            billingaddress = BillingAddress.objects.get(user=request.user)

            billingaddress_form = BillingAddressFrom(request.POST, instance=billingaddress)
            profile_obj = Profile.objects.get(user=request.user)
            profileForm = ProfileForm(request.POST, instance=profile_obj)
            if billingaddress_form.is_valid() or profileForm.is_valid():
                billingaddress_form.save()
                profileForm.save()
                return redirect('account:profile')
