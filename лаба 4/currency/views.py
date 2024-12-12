from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .models import Currency
from .forms import CurrencyForm

def upd_cur():
    try:
        from currency.models import Currency


        for i in settings.AVAILABLE_CURRENCIES:
                Currency.objects.update_or_create(**i)
    except Exception as e:
        print(e)
        pass

upd_cur()
    

def UserLogin(request):
    context = {
        'title': 'Login',
        'pageTitle': 'Login',
        'btn': 'Login'
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('currency:index')
        else:
            context['error'] = 'Invalid Username or Password'
            return render(request, 'logauth/login.html', context)
    return render(request, 'logauth/login.html', context)

def UserLogout(request):
    logout(request)
    return redirect('currency:login')

def UserRegister(request):
    context = {
        'title': 'Register',
        'pageTitle': 'Register',
        'btn': 'Create'
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            context['error'] = 'Username already exists'
            return render(request, 'logauth/login.html', context)
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('currency:index')
    else:
        return render(request, 'logauth/login.html', context)
        

def index(request):
    if not(request.user.is_authenticated):
        return redirect('currency:login')
        
    context = {
        'pageTitle': 'Currency Exchange',
        'currencies': Currency.objects.all(),
        'Val' : {i.CharCode : {"Value" : i.Value, "Nominal": i.Nominal} for i in Currency.objects.all()}
    }
    return render(request, 'currency/index.html', context)

# Create your views here.
