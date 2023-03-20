from django.db import models
from product.models import Product
from accounts.models import CustomUser
from django.utils import timezone

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateField(default=timezone.now, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=None, null=True)

    def total_price(self):
        if self.price is not None:
            return self.quantity * self.price
        else:
            return 0.0

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def total_price(self):
        cart_items = self.items.all()
        total_price = sum(item.total_price() for item in cart_items)
        return total_price
    
    def get_total_price(self):
        return '{:.2f}'.format(self.total_price())
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Order ({self.date_ordered.strftime('%b %d, %Y %I:%M %p')})"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=None, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        if self.price is not None:
            return self.quantity * self.price
        else:
            return 0.0



    
class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)



