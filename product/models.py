from django.db import models
from django.contrib.auth import get_user_model
from django import forms

CustomUser = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        app_label = 'product'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    Category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    inventory = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True)

    def get_reviews(self):
        return self.reviews.all()

    class Meta:
        ordering = ('-created_at',)

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.value for rating in ratings) / len(ratings)
        else:
            return None

    def get_reviews(self):
        return self.reviews.all()
    
    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"


    def decrease_quantity(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        else:
            return False





class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username}\'s rating of {self.product.name}: {self.value}'
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username}\'s review of {self.product.name}'

    

class ReviewForm(forms.Form):
    rating_choices = [(i, i) for i in range(1, 6)]
    rating = forms.ChoiceField(choices=rating_choices, label='Rating', widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Comment')
# Create your models here.
