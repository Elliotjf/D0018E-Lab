from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, Cart, Wallet, Order, OrderItem
from product.models import Product, Inventory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from decimal import Decimal
from django.contrib import messages
from django.db import transaction

CustomUser = get_user_model()

@login_required
def checkoutRedirect(request):
    # Retrieve the cart for the current user
    cart = Cart.objects.get(user=request.user)
    

    # Check if the cart has items
    if not cart.items.exists():
        return redirect('cart:view_cart')

    # Retrieve the cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the total price of the cart items
    total_price = cart.total_price()

    # Retrieve the user's wallet balance
    wallet = Wallet.objects.get(user=request.user)
    balance = wallet.balance

    # Render the checkout template with the cart items and total price
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'balance': balance})



@transaction.atomic
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=CustomUser.objects.get(id=request.user.id),
        defaults={'quantity': 1, 'price': product.price},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart, created = Cart.objects.get_or_create(user=CustomUser.objects.get(id=request.user.id))
    cart.items.add(cart_item)

    return redirect('cart:view_cart')

@transaction.atomic
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, user=CustomUser.objects.get(id=request.user.id))
    cart_item.delete()
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=CustomUser.objects.get(id=request.user.id))
        cart_items = cart.items.all()
        if cart_items:
            total_price = cart.get_total_price()
            return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
        else:
            message = "There are no items in your cart."
            return render(request, 'emptyCart.html', {'message': message})
    except Cart.DoesNotExist:
        message = "There are no items in your cart."
        return render(request, 'emptyCart.html', {'message': message})
    except AttributeError:
        message = "You need to be logged in to view your cart."
        return render(request, 'emptyCart.html', {'message': message})

@transaction.atomic    
@login_required
def add_funds(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += amount
        wallet.save()
        return redirect('cart:view_cart')

    return render(request, 'add_funds.html')

@receiver(user_signed_up)
def create_wallet(sender, user, request, **kwargs):
    wallet = Wallet(user=user)
    wallet.save()

@receiver(user_logged_in)
def check_wallet(sender, user, request, **kwargs):
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        wallet = Wallet(user=user)
        wallet.save()

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

@transaction.atomic
@login_required
def checkout(request):
    # Get the user's cart
    cart = Cart.objects.get(user=request.user)

    # Check if the cart has items
    if not cart.items.exists():
        return redirect('cart:view_cart')
    else:
        # Get the user's wallet
        wallet = Wallet.objects.get(user=request.user)

        # Calculate the cart total and check if the user has sufficient balance
        cart_total = cart.total_price()
        if wallet.balance < cart_total:
            messages.error(request, "Insufficient balance")
            return redirect('cart:add_funds')

        # Create a new order instance
        # Create a list of cart items
        cart_items = cart.items.all()

        # Create a new order instance and set the items field to the list of cart items
        order = Order.objects.create(user=request.user, total_price=cart_total)
        for item in cart_items:
            if item.quantity > item.product.inventory:
                messages.error(request, f"Insufficient inventory for {item.product.name}")
                return redirect('cart:view_cart')
            item.product.inventory -= item.quantity
            item.product.save()
            order_item = OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.price)
            order_item.save()
        

        # Deduct the cart total from the user's balance and clear the user's cart
        wallet.balance -= cart_total
        wallet.save()
        cart_items.delete()
        cart.items.clear()

        messages.success(request, "Order placed successfully")
        return redirect('cart:order_complete')

