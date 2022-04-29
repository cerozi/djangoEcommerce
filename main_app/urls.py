from django.urls import path
from .views import CheckoutView, HomeTemplate, ProductTemplate, addToCart, removeFromCart, CartSummaryView, removeCart

urlpatterns = [
    path('', HomeTemplate.as_view(), name='home'),
    path('product/<slug:slug>/', ProductTemplate.as_view(), name='product'),
    path('add-to-cart/<slug:slug>', addToCart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>', removeFromCart, name='remove-from-cart'),
    path('remove-cart/<slug:slug>', removeCart, name='remove-cart'),
    path('cart/', CartSummaryView.as_view(), name='cart-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

]