from django.http import HttpResponse
from product.models import Product
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from product.models import ReviewForm, Review


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

#def product_detail(request, pk):
 # product = Product.objects.get(pk=pk)
  #return render(request, 'product_detail.html', {'product': product})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    review_form = ReviewForm()

    user_reviewed = reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid() and not user_reviewed:
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'product_detail.html', context)

def product_list(request):
  products = Product.objects.all()
  return render(request, 'products.html', {'products': products})
