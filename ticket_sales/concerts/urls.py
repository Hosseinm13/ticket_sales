from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]