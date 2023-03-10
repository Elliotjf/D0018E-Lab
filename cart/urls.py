from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart, add_funds, checkout, checkoutRedirect, order_history

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('', view_cart, name='view_cart'),
    path('add-funds/', add_funds, name='add_funds'),
    path('checkout/', checkoutRedirect, name='checkout'),
    path('order_complete/', checkout, name='order_complete'),
    path('order-history/', order_history, name='order_history'),
]