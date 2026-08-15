from django.urls import path
from . import views

urlpatterns = [

    # ========================== 
    # Dashboard 
    # ========================== 

    path(
        '',
        views.dashboard,
        name="dashboard"
    ),

    # ==========================
    # Users
    # ==========================

    path(
        'users/',
        views.users,
        name="users"
    ),

    # ========================== 
    # Pending Posts 
    # ========================== 

    path(
        'posts/',
        views.posts,
        name="posts"
    ),

    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name="post_detail"
    ),

    path(
        'posts/<int:post_id>/approve/',
        views.approve_post,
        name="approve_post"
    ),

    path(
        'posts/<int:post_id>/reject/',
        views.reject_post,
        name="reject_post"
    ),

    # ==========================
    # Wallet Requests 
    # ========================== 

    path(
        'wallet/',
        views.wallet_requests,
        name="wallet_requests"
    ),

    path(
        'wallet/approve/<int:deposit_id>/',
        views.approve_deposit,
        name="approve_deposit"
    ),

    path(
        'wallet/reject/<int:deposit_id>/',
        views.reject_deposit,
        name="reject_deposit"
    ),

    # ==========================
    # Notifications 
    # ========================== 

    path(
        "notifications/read/<int:noti_id>/",
        views.read_notification,
        name="read_notification"
    ),

    path(
        "wallet/deposits/",
        views.deposit_requests,
        name="deposit_requests",
    ),

    path(
        "wallet/deposit/<int:deposit_id>/approve/",
        views.approve_deposit,
        name="approve_deposit",
    ),

    path(
        "wallet/deposit/<int:deposit_id>/reject/",
        views.reject_deposit,
        name="reject_deposit",
    ),

    path(
        "wallet/withdraws/",
        views.withdraw_requests,
        name="withdraw_requests",
    ),

    path(
        "wallet/withdraws/<int:withdraw_id>/approve/",
        views.approve_withdraw,
        name="approve_withdraw",
    ),

    path(
        "wallet/withdraws/<int:withdraw_id>/reject/",
        views.reject_withdraw,
        name="reject_withdraw",
    ),

    path(
        'wallet/withdraw/approve/<int:withdraw_id>/',
        views.approve_withdraw,
        name="approve_withdraw"
    ),

    path(
        'wallet/withdraw/reject/<int:withdraw_id>/',
        views.reject_withdraw,
        name="reject_withdraw"
    ),

    path(
        "users/<int:user_id>/ban/",
        views.ban_user,
        name="ban_user",
    ),

    path(
        "users/<int:user_id>/unban/",
        views.unban_user,
        name="unban_user",
    ),

    # All Orders
    path('orders/', views.orders, name='admin_orders'),

    # Orders by status
    path('orders/pending/', views.pending_orders, name='admin_pending_orders'),
    path('orders/ready/', views.ready_for_pickup_orders, name='admin_ready_orders'),
    path('orders/picked-up/', views.picked_up_orders, name='admin_picked_up_orders'),
    path('orders/completed/', views.completed_orders, name='admin_completed_orders'),
    path('orders/cancelled/', views.cancelled_orders, name='admin_cancelled_orders'),

    # Order detail and actions
    path('orders/<int:order_id>/', views.order_detail, name='admin_order_detail'),
    path('orders/<int:order_id>/<str:new_status>/', views.update_order_status, name='admin_update_order_status'),

]