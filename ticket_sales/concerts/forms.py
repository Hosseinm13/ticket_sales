from django import forms
from .models import Concert, Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'artist', 'date', 'location', 'price', 'image', 'available_tickets']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['quantity']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']