from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Rating
from .models import ReviewForm
from django.contrib.auth.decorators import login_required

#def add_review(request, slug):
   # product = get_object_or_404(Product, slug=slug)

   # if request.method == 'POST':
    #    form = ReviewForm(request.POST)
      #  if form.is_valid():
       #     rating = form.cleaned_data['rating']
       #     comment = form.cleaned_data['comment']
         #   review = Review(product=product, user=request.user, comment=comment)
         #   review.save()
        #    Review.objects.create(product=product, user=request.user, rating=int(rating))
         #   return redirect('product_detail', slug=slug)
  #  else:
     #   form = ReviewForm()
#
   # return render(request, 'review.html', {'product': product, 'form': form})

@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Create a new Rating object
            rating = Rating(product=product, user=request.user, value=rating_value)
            rating.save()

            # Create a new Review object
            review = Review(product=product, user=request.user, rating=rating, comment=comment)
            review.save()

            return redirect('product_detail', slug=product.slug)

    context = {
        'product': product,
        'form': form
    }

    return render(request, 'review.html', {'product': product, 'form': form})

