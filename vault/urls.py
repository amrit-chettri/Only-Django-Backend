from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
]