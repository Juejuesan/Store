from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('count/', views.cart_count, name='cart_count'),
]