from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from concerts.models import Ticket
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'حساب کاربری {username} با موفقیت ساخته شد!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'برای دسترسی به پروفایل باید وارد شوید.')
        return redirect('login')
    tickets = Ticket.objects.filter(user=request.user)
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    return render(request, 'accounts/profile.html', {'tickets': tickets, 'profile': profile})