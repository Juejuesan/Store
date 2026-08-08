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

]