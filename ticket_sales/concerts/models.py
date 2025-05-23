from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='concerts/', blank=True)
    available_tickets = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.concert.title}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سبد خرید {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} بلیط برای {self.concert.title}"

    def get_total_price(self):
        return self.quantity * self.concert.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"سفارش {self.id} - {self.user.username}"