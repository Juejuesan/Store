from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from posts.models import Post
from notifications.models import Notification

from wallet.models import (
    DepositRequest,
    Wallet,
    WalletTransaction,
)
# ==========================
# Dashboard
# ==========================
def dashboard(request):
    context = {
        "total_users": User.objects.filter(is_active=True).count(),
        "total_sellers": User.objects.count(),
        "pending_posts": Post.objects.filter(
            status="pending"
        ).count(),
        "pending_orders": 15,
        "total_revenue": "15,800,000",
        "recent_activities": [
            {
                "activity": "New Seller Registered",
                "user": "Ko Ko",
                "status": "Success",
                "time": "2 mins ago",
            },
            {
                "activity": "Product Submitted",
                "user": "Su Su",
                "status": "Pending",
                "time": "10 mins ago",
            },
            {
                "activity": "Wallet Top Up",
                "user": "Mg Mg",
                "status": "Completed",
                "time": "35 mins ago",
            },
            {
                "activity": "Account Warning",
                "user": "Aung Aung",
                "status": "Warning",
                "time": "1 hour ago",
            },
        ],
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
    )
# ==========================
# Wallet Deposit Requests
# ==========================

@login_required
def wallet_requests(request):

    deposits = DepositRequest.objects.all().order_by(
        "-created_at"
    )


    pending_count = DepositRequest.objects.filter(
        status="Pending"
    ).count()


    approved_amount = sum(
        DepositRequest.objects.filter(
            status="Approved"
        ).values_list(
            "amount",
            flat=True
        )
    )


    context = {

        "deposits": deposits,

        "pending_count": pending_count,

        "approved_amount": approved_amount,

    }


    return render(
        request,
        "adminpanel/wallet.html",
        context
    )
# ==========================
# Approve Deposit
# ==========================

@login_required
def approve_deposit(request, deposit_id):

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )


    if deposit.status == "Pending":


        deposit.status = "Approved"

        deposit.approved_at = timezone.now()

        deposit.approved_by = request.user

        deposit.save()



        # Add money to wallet

        wallet, created = Wallet.objects.get_or_create(
            user=deposit.user
        )


        wallet.balance += deposit.amount

        wallet.save()



        # Transaction history

        WalletTransaction.objects.create(

            wallet=wallet,

            transaction_type="Deposit",

            amount=deposit.amount,

            status="Approved",

            description="Deposit approved by admin",

            reference_id=str(deposit.id)

        )



        # User notification

        Notification.objects.create(

            user=deposit.user,

            message=f"Your wallet has been credited {deposit.amount} MMK added successfully.",

            notification_type="deposit_approved"

        )


    return redirect(
        "wallet_requests"
    )
# ==========================
# Reject Deposit
# ==========================

@login_required
def reject_deposit(request, deposit_id):

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )


    if deposit.status == "Pending":


        deposit.status = "Rejected"

        deposit.save()

        Notification.objects.create(
            user=deposit.user,
            message=f"Your wallet deposit request of {deposit.amount} MMK was rejected.",
            notification_type="deposit_rejected"
        )


    return redirect(
        "wallet_requests"
    )
# ==========================
# Pending Posts
# ==========================
def posts(request):
    pending_posts = Post.objects.filter(
        status="pending"
    ).order_by("-created_at")

    context = {
        "pending_posts": pending_posts,
    }

    return render(
        request,
        "adminpanel/posts.html",
        context,
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(
        request,
        "adminpanel/post_detail.html",
        {
            "post": post,
        },
    )


def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.status = "approved"
    post.save()

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been approved.",
        notification_type="approved",
    )

    return redirect("posts")


def reject_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.status = "rejected"
    post.save()

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been rejected.",
        notification_type="rejected",
    )

    return redirect("posts")

from django.contrib.auth.decorators import login_required

@login_required
def read_notification(request, noti_id):

    notification = get_object_or_404(
        Notification,
        id=noti_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    if notification.notification_type == "new_post":
        return redirect("posts")

    return redirect("dashboard")