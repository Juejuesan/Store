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

]