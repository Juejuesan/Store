from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from posts.models import Post
from notifications.models import Notification
from django.contrib import messages
from wallet.models import (
    DepositRequest,
    WithdrawRequest,
    Wallet,
    WalletTransaction,
)
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

@transaction.atomic
def approve_deposit(request, deposit_id):

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    # Prevent approving twice
    if deposit.status != "Pending":
        return redirect("deposit_requests")

    wallet, created = Wallet.objects.get_or_create(
        user=deposit.user
    )

    # Add balance
    wallet.balance += deposit.amount
    wallet.save()

    # Update request
    deposit.status = "Approved"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    # Save transaction history
    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Deposit",
        amount=deposit.amount,
        status="Approved",
        description="Wallet deposit approved by admin.",
        reference_id=str(deposit.id),
    )

    # Send notification
    Notification.objects.create(
        user=deposit.user,
        message=f"Your deposit of MMK {deposit.amount:,.0f} has been approved.",
        notification_type="deposit_approved",
    )

    return redirect("deposit_requests")




@transaction.atomic
def reject_deposit(request, deposit_id):

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    if deposit.status != "Pending":
        return redirect("deposit_requests")

    deposit.status = "Rejected"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    Notification.objects.create(
        user=deposit.user,
        message="Your deposit request has been rejected.",
        notification_type="deposit_rejected",
    )

    return redirect("deposit_requests")



def deposit_requests(request):

    deposits = DepositRequest.objects.select_related(
        "user"
    ).order_by("-created_at")

    pending_count = deposits.filter(
        status="Pending"
    ).count()

    approved_amount = (
        deposits.filter(
            status="Approved"
        )
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    context = {

        "deposits": deposits,

        "pending_count": pending_count,

        "approved_amount": approved_amount,

    }

    return render(
        request,
        "adminpanel/deposit_requests.html",
        context,
    )


# =====================================================
# Dashboard
# =====================================================

@login_required
def dashboard(request):

    context = {

        "total_users": User.objects.filter(
            is_active=True
        ).count(),

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

        ],

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
    )


# =====================================================
# Wallet Requests
# =====================================================

@login_required
def wallet_requests(request):

    deposits = DepositRequest.objects.all().order_by("-created_at")

    withdrawals = WithdrawRequest.objects.all().order_by("-created_at")

    pending_deposits = DepositRequest.objects.filter(
        status="Pending"
    ).count()

    pending_withdrawals = WithdrawRequest.objects.filter(
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

    approved_withdraw_amount = sum(
        WithdrawRequest.objects.filter(
            status="Approved"
        ).values_list(
            "amount",
            flat=True
        )
    )

    context = {

        "deposits": deposits,

        "withdrawals": withdrawals,

        "pending_count": pending_deposits,

        "pending_withdrawals": pending_withdrawals,

        "approved_amount": approved_deposit_amount,

        "approved_withdraw_amount": approved_withdraw_amount,

    }

    return render(
        request,
        "adminpanel/wallet.html",
        context,
    )


@login_required
def approve_withdraw(request, withdraw_id):

    withdraw = get_object_or_404(
        WithdrawRequest,
        id=withdraw_id
    )

    if withdraw.status == "Pending":

        wallet = get_object_or_404(
            Wallet,
            user=withdraw.user
        )

        if withdraw.amount > wallet.balance:

            Notification.objects.create(
                user=withdraw.user,
                message=(
                    f"Your withdrawal request of "
                    f"{withdraw.amount} MMK was rejected "
                    f"because of insufficient wallet balance."
                ),
                notification_type="withdraw_rejected",
            )

            withdraw.status = "Rejected"
            withdraw.admin_remark = (
                "Insufficient wallet balance."
            )
            withdraw.save()

            return redirect("wallet_requests")

        wallet.balance -= withdraw.amount
        wallet.save()

        withdraw.status = "Approved"
        withdraw.approved_at = timezone.now()
        withdraw.approved_by = request.user
        withdraw.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type="Withdraw",
            amount=withdraw.amount,
            status="Approved",
            description="Withdrawal approved by admin",
            reference_id=str(withdraw.id)
        )

        Notification.objects.create(
            user=withdraw.user,
            message=(
                f"Your withdrawal request of "
                f"{withdraw.amount} MMK has been approved."
            ),
            notification_type="withdraw_approved",
        )

    return redirect("wallet_requests")

@login_required
def reject_withdraw(request, withdraw_id):

    withdraw = get_object_or_404(
        WithdrawRequest,
        id=withdraw_id
    )

    if withdraw.status == "Pending":

        withdraw.status = "Rejected"
        withdraw.approved_by = request.user
        withdraw.save()

        Notification.objects.create(
            user=withdraw.user,
            message=(
                f"Your withdrawal request of "
                f"{withdraw.amount} MMK was rejected."
            ),
            notification_type="withdraw_rejected",
        )

    return redirect("wallet_requests")
# =====================================================
# Approve Deposit
# =====================================================

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

        wallet, created = Wallet.objects.get_or_create(
            user=deposit.user
        )

        wallet.balance += deposit.amount
        wallet.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type="Deposit",
            amount=deposit.amount,
            status="Approved",
            description="Deposit approved by admin",
            reference_id=str(deposit.id)
        )

        Notification.objects.create(
            user=deposit.user,
            message=f"Your wallet has been credited {deposit.amount} MMK.",
            notification_type="deposit_approved",
        )

    return redirect("wallet_requests")


# =====================================================
# Reject Deposit
# =====================================================

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
            message=f"Your deposit request of {deposit.amount} MMK was rejected.",
            notification_type="deposit_rejected",
        )

    return redirect("wallet_requests")


# =====================================================
# Pending Posts
# =====================================================

@login_required
def posts(request):

    pending_posts = Post.objects.filter(
        status="pending"
    ).order_by("-created_at")

    return render(
        request,
        "adminpanel/posts.html",
        {
            "pending_posts": pending_posts,
        },
    )


# =====================================================
# Post Detail
# =====================================================

@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    return render(
        request,
        "adminpanel/post_detail.html",
        {
            "post": post,
        },
    )


# =====================================================
# Approve Post
# =====================================================

@login_required
def approve_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    post.status = "approved"
    post.save()

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been approved.",
        notification_type="approved",
    )

    return redirect("posts")


# =====================================================
# Reject Post
# =====================================================

@login_required
def reject_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    post.status = "rejected"
    post.save()

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been rejected.",
        notification_type="rejected",
    )

    return redirect("posts")


# =====================================================
# Read Notification
# =====================================================

@login_required
def read_notification(request, noti_id):

    notification = get_object_or_404(
        Notification,
        id=noti_id,
        user=request.user,
    )

    notification.is_read = True
    notification.save()

    return redirect("dashboard")

# ==========================================
# Withdrawal Requests
# ==========================================

def withdraw_requests(request):

    withdrawals = WithdrawRequest.objects.select_related(
        "user"
    ).order_by("-created_at")

    pending_count = withdrawals.filter(
        status="Pending"
    ).count()

    approved_amount = sum(
        w.amount
        for w in withdrawals.filter(status="Approved")
    )

    context = {

        "withdrawals": withdrawals,

        "pending_count": pending_count,

        "approved_amount": approved_amount,

    }

    return render(
        request,
        "adminpanel/withdraw_requests.html",
        context,
    )

#
# # ==========================================
# # Approve Withdrawal
# # ==========================================
#
# def approve_withdraw(request, withdraw_id):
#
#     withdraw = get_object_or_404(
#
#         WithdrawRequest,
#
#         id=withdraw_id
#
#     )
#
#     if withdraw.status == "Pending":
#
#         wallet = get_object_or_404(
#
#             Wallet,
#
#             user=withdraw.user
#
#         )
#
#         if wallet.balance >= withdraw.amount:
#
#             wallet.balance -= withdraw.amount
#
#             wallet.save()
#
#             WalletTransaction.objects.create(
#
#                 wallet=wallet,
#
#                 transaction_type="Withdraw",
#
#                 amount=withdraw.amount,
#
#                 status="Approved",
#
#                 description="Withdrawal approved by admin",
#
#                 reference_id=str(withdraw.id),
#
#             )
#
#             withdraw.status = "Approved"
#
#             withdraw.approved_by = request.user
#
#             withdraw.approved_at = timezone.now()
#
#             withdraw.save()
#
#             # Optional Notification
#             # Notification.objects.create(
#             #     user=withdraw.user,
#             #     message="Your withdrawal request has been approved.",
#             # )
#
#     return redirect("withdraw_requests")
#
#
# def reject_withdraw(request, withdraw_id):
#
#     withdraw = get_object_or_404(
#         WithdrawRequest,
#         id=withdraw_id
#     )
#
#     if withdraw.status != "Pending":
#
#         messages.warning(
#             request,
#             "This withdrawal request has already been processed."
#         )
#
#         return redirect("withdraw_requests")
#
#     withdraw.status = "Rejected"
#
#     withdraw.approved_at = timezone.now()
#
#     withdraw.approved_by = request.user
#
#     withdraw.save()
#
#     WalletTransaction.objects.create(
#         wallet=withdraw.user.wallet,
#         transaction_type="Withdraw",
#         amount=withdraw.amount,
#         status="Rejected",
#         description="Withdrawal request rejected by admin.",
#         reference_id=f"WD-{withdraw.id}"
#     )
#
#     Notification.objects.create(
#         user=withdraw.user,
#         message=(
#             f"Your withdrawal request of "
#             f"{withdraw.amount} MMK has been rejected."
#         ),
#         notification_type="withdraw_rejected",
#     )
#
#     messages.success(
#         request,
#         "Withdrawal request rejected successfully."
#     )
#
#     return redirect("withdraw_requests")