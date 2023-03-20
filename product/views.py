from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Rating
from .models import ReviewForm
from  cart.models import OrderItem
from django.contrib.auth.decorators import login_required
from django.db import transaction


@transaction.atomic
@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Check if user has purchased the product
            if OrderItem.objects.filter(order__user=request.user, product=product).exists():
                # Check if user has already left a review
                if Review.objects.filter(product=product, user=request.user).exists():
                    # User has already left a review, show an error message
                    form.add_error(None, "You have already left a review for this product.")
                else:
                    # Create a new Rating object
                    rating = Rating(product=product, user=request.user, value=rating_value)
                    rating.save()

                    # Create a new Review object
                    review = Review(product=product, user=request.user, rating=rating, comment=comment)
                    review.save()

                    return redirect('product_detail', slug=product.slug)
            else:
                # User has not purchased the product, show an error message
                form.add_error(None, "You must purchase this item before leaving a review.")

    context = {
        'product': product,
        'form': form
    }

    return render(request, 'review.html', context)
