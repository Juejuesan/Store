from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    # Buyer URLs
    path('purchase/', views.purchase_cart, name='purchase_cart'),
    path('orders/', views.order_list, name='order_list'),
path('orders/<int:order_id>/confirm-pickup/', views.confirm_seller_pickup, name='confirm_seller_pickup'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/picked-up/', views.mark_picked_up, name='mark_picked_up'),


    # Seller URLs
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/orders/<int:order_id>/ready/', views.mark_ready_for_pickup, name='mark_ready_for_pickup'),
    path('seller/orders/<int:order_id>/completed/', views.mark_completed, name='mark_completed'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/<int:order_id>/', views.sale_detail, name='sale_detail'),
]