from django.urls import path
from cart.views import AddToCart, RemoveFromCart

app_name = 'cart'

urlpatterns = [
    path('add', AddToCart.as_view(), name='add'),
    path('remove', RemoveFromCart.as_view(), name='remove'),
]
