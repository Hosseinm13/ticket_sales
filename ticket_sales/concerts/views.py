from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Concert, Cart, CartItem, Order, Ticket
from django.db.models import Q

def home(request):
    concerts = Concert.objects.all()
    location = request.GET.get('location')
    artist = request.GET.get('artist')
    search_query = request.GET.get('search')

    if location and location != 'همه شهرها':
        concerts = concerts.filter(location=location)
    if artist and artist != 'همه هنرمندان':
        concerts = concerts.filter(artist=artist)
    if search_query:
        concerts = concerts.filter(
            Q(title__icontains=search_query) | Q(artist__icontains=search_query)
        )

    locations = Concert.objects.values_list('location', flat=True).distinct()
    artists = Concert.objects.values_list('artist', flat=True).distinct()

    return render(request, 'index.html', {
        'concerts': concerts,
        'locations': locations,
        'artists': artists,
        'selected_location': location,
        'selected_artist': artist,
        'search_query': search_query,
    })

def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'برای افزودن به سبد خرید باید وارد شوید.')
            return redirect('login')
        quantity = int(request.POST.get('quantity', 1))
        if quantity > concert.available_tickets:
            messages.error(request, 'تعداد بلیط درخواستی بیشتر از موجودی است.')
            return redirect('concert_detail', concert_id=concert.id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, concert=concert, defaults={'quantity': quantity}
        )
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, 'بلیط به سبد خرید اضافه شد.')
        return redirect('cart')
    return render(request, 'concerts/concert_detail.html', {'concert': concert})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        if action == 'increase':
            if item.quantity + 1 <= item.concert.available_tickets:
                item.quantity += 1
                item.save()
            else:
                messages.error(request, 'موجودی کافی نیست.')
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        elif action == 'remove':
            item.delete()
        return redirect('cart')
    total_price = sum(item.get_total_price() for item in cart.items.all())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('cart')
    total_price = sum(item.get_total_price() for item in cart.items.all())
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.items.all():
            concert = item.concert
            if item.quantity > concert.available_tickets:
                messages.error(request, f'موجودی بلیط برای {concert.title} کافی نیست.')
                order.delete()
                return redirect('cart')
            concert.available_tickets -= item.quantity
            concert.save()
            Ticket.objects.create(
                user=request.user,
                concert=concert,
                quantity=item.quantity
            )
        order.is_paid = True
        order.save()
        cart.items.all().delete()
        messages.success(request, 'پرداخت با موفقیت انجام شد.')
        return redirect('home')
    return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price})