from django.urls import path
from . import views

urlpatterns = [
    path('my_wishlist/', views.wishlist, name='wishlist'),
    path('add/<int:product_id>', views.add_to_wishlist, name='add_to_wishlist'),
]