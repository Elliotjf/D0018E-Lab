from django.urls import path, include
from . import views
from .views import product_detail, product_list
from accounts.views import register, login_view, logout_view
from product.views import add_review


urlpatterns = [
    path('', views.main, name='main'),
 #   path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    path('products/', product_list, name='product_list'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cart/', include('cart.urls')),
    path('product/<slug:slug>/review/', add_review, name='review'),
]

