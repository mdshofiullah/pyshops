from django.shortcuts import render
from django.http import HttpResponse

from account.forms import RegistrationForm

# Authentication function
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


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
            'form' : form
        }
    return render(request, 'register.html', context)


def Customerlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('Your just logged in')
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username = username, password = password)
            if customer is not None:
                login(request, customer)
                return HttpResponse('you logged in successfully!')
            else:
                return HttpResponse('404')

    return render(request, 'login.html')
