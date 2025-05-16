from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Concert, Ticket
from .forms import ConcertForm, TicketForm, UserRegisterForm
from django.contrib.auth.models import User

def home(request):
    concerts = Concert.objects.all()
    return render(request, 'index.html', {'concerts': concerts})

def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= concert.available_tickets:
                Ticket.objects.create(
                    user=request.user,
                    concert=concert,
                    quantity=quantity
                )
                concert.available_tickets -= quantity
                concert.save()
                return redirect('payment', concert_id=concert.id)
            else:
                messages.error(request, 'تعداد بلیط درخواستی بیشتر از موجودی است.')
    else:
        form = TicketForm()
    return render(request, 'concert_detail.html', {'concert': concert, 'form': form})

@login_required
def payment(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        messages.success(request, 'پرداخت با موفقیت انجام شد!')
        return redirect('home')
    return render(request, 'payment.html', {'concert': concert})

@user_passes_test(lambda u: u.is_staff)
def admin_concert(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'کنسرت با موفقیت اضافه شد.')
            return redirect('admin_concert')
    else:
        form = ConcertForm()
    concerts = Concert.objects.all()
    return render(request, 'admin_concert.html', {'form': form, 'concerts': concerts})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')