from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from order.models import Order, OrderItem


from user.models import Profile
from posts.models import Post
from notifications.models import Notification
from wallet.models import (
    DepositRequest,
    WithdrawRequest,
    Wallet,
    WalletTransaction,
)

from .models import AdminActivity


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):
    recent_activities = AdminActivity.objects.select_related(
        "admin"
    ).order_by("-created_at")[:10]

    context = {

        "total_users": User.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True
        ).count(),

        "total_sellers": User.objects.filter(
            is_staff=False,
            is_superuser=False
        ).count(),

        "pending_posts": Post.objects.filter(
            status="pending"
        ).count(),

        "pending_orders": 15,

        "total_revenue": "15,800,000",

        "recent_activities": recent_activities,
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )


# =========================================================
# USERS
# =========================================================

@login_required
def users(request):
    users = (
        User.objects
        .filter(
            is_staff=False,
            is_superuser=False
        )
        .select_related("profile")
        .order_by("-date_joined")
    )

    context = {
        "users": users,
        "total_users": users.count(),
    }

    return render(
        request,
        "adminpanel/user.html",
        context
    )


# =========================================================
# BAN USER
# =========================================================

@login_required
def ban_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id
    )

    profile = get_object_or_404(
        Profile,
        user=user
    )

    profile.status = "Banned"
    profile.save()

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="ban_user",
        message=f"You successfully banned {user.username}"
    )

    messages.success(
        request,
        f"{user.username} has been banned successfully."
    )

    return redirect("users")


# =========================================================
# UNBAN USER
# =========================================================

@login_required
def unban_user(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id
    )

    profile = get_object_or_404(
        Profile,
        user=user
    )

    profile.status = "Approved"
    profile.save()

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="unban_user",
        message=f"You successfully unbanned {user.username}"
    )

    messages.success(
        request,
        f"{user.username} has been unbanned successfully."
    )

    return redirect("users")


# =========================================================
# PENDING POSTS
# =========================================================

@login_required
def posts(request):
    pending_posts = (
        Post.objects
        .filter(status="pending")
        .select_related("user")
        .order_by("-created_at")
    )

    return render(
        request,
        "adminpanel/posts.html",
        {
            "pending_posts": pending_posts,
        }
    )


# =========================================================
# POST DETAIL
# =========================================================

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    return render(
        request,
        "adminpanel/post_detail.html",
        {
            "post": post,
        }
    )


# =========================================================
# APPROVE POST
# =========================================================

@login_required
def approve_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    post.status = "approved"
    post.save()

    # Get seller username safely
    try:
        username = post.user.user.username
    except AttributeError:
        username = "user"

        # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="approve_post",
        message=f"You successfully approved a post from {username}"
    )

    # USER NOTIFICATION
    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been approved.",
        notification_type="approved",
    )

    messages.success(
        request,
        "Post approved successfully."
    )

    return redirect("posts")


# =========================================================
# REJECT POST
# =========================================================

@login_required
def reject_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    post.status = "rejected"
    post.save()

    try:
        username = post.user.user.username
    except AttributeError:
        username = "user"

        # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="reject_post",
        message=f"You successfully rejected a post from {username}"
    )

    # USER NOTIFICATION
    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been rejected.",
        notification_type="rejected",
    )

    messages.success(
        request,
        "Post rejected successfully."
    )

    return redirect("posts")


# =========================================================
# WALLET PAGE
# =========================================================

@login_required
def wallet_requests(request):
    deposits = (
        DepositRequest.objects
        .select_related("user")
        .order_by("-created_at")
    )

    withdrawals = (
        WithdrawRequest.objects
        .select_related("user")
        .order_by("-created_at")
    )

    pending_deposits = deposits.filter(
        status="Pending"
    ).count()

    pending_withdrawals = withdrawals.filter(
        status="Pending"
    ).count()

    approved_amount = (
            deposits
            .filter(status="Approved")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
    )

    approved_withdraw_amount = (
            withdrawals
            .filter(status="Approved")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
    )

    context = {

        "deposits": deposits,

        "withdrawals": withdrawals,

        "pending_count": pending_deposits,

        "pending_withdrawals": pending_withdrawals,

        "approved_amount": approved_amount,

        "approved_withdraw_amount": approved_withdraw_amount,
    }

    return render(
        request,
        "adminpanel/wallet.html",
        context
    )


# =========================================================
# DEPOSIT REQUESTS
# =========================================================

@login_required
def deposit_requests(request):
    deposits = (
        DepositRequest.objects
        .select_related("user")
        .order_by("-created_at")
    )

    pending_count = deposits.filter(
        status="Pending"
    ).count()

    approved_amount = (
            deposits
            .filter(status="Approved")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
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


# =========================================================
# APPROVE DEPOSIT
# =========================================================

@login_required
@transaction.atomic
def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    # Prevent approving twice
    if deposit.status != "Pending":
        messages.warning(
            request,
            "This deposit request has already been processed."
        )

        return redirect("deposit_requests")

        # Get or create wallet
    wallet, created = Wallet.objects.get_or_create(
        user=deposit.user
    )

    # Add money
    wallet.balance += deposit.amount
    wallet.save()

    # Update deposit
    deposit.status = "Approved"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    # Transaction history
    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Deposit",
        amount=deposit.amount,
        status="Approved",
        description="Deposit approved by admin",
        reference_id=str(deposit.id),
    )

    # User notification
    Notification.objects.create(
        user=deposit.user,
        message=(
            f"Your deposit of "
            f"MMK {deposit.amount:,.0f} "
            f"has been approved."
        ),
        notification_type="deposit_approved",
    )

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="approve_deposit",
        message=(
            f"You successfully approved a deposit "
            f"of MMK {deposit.amount:,.0f} "
            f"from {deposit.user.username}"
        )
    )

    messages.success(
        request,
        "Deposit approved successfully."
    )

    return redirect("deposit_requests")


# =========================================================
# REJECT DEPOSIT
# =========================================================

@login_required
@transaction.atomic
def reject_deposit(request, deposit_id):
    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    if deposit.status != "Pending":
        messages.warning(
            request,
            "This deposit request has already been processed."
        )

        return redirect("deposit_requests")

    deposit.status = "Rejected"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    # User notification
    Notification.objects.create(
        user=deposit.user,
        message=(
            f"Your deposit request of "
            f"MMK {deposit.amount:,.0f} "
            f"was rejected."
        ),
        notification_type="deposit_rejected",
    )

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="reject_deposit",
        message=(
            f"You successfully rejected a deposit "
            f"of MMK {deposit.amount:,.0f} "
            f"from {deposit.user.username}"
        )
    )

    messages.success(
        request,
        "Deposit rejected successfully."
    )

    return redirect("deposit_requests")


# =========================================================
# WITHDRAW REQUESTS
# =========================================================

@login_required
def withdraw_requests(request):
    withdrawals = (
        WithdrawRequest.objects
        .select_related("user")
        .order_by("-created_at")
    )

    pending_count = withdrawals.filter(
        status="Pending"
    ).count()

    approved_amount = (
            withdrawals
            .filter(status="Approved")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
    )

    context = {

        "withdrawals": withdrawals,

        "pending_count": pending_count,

        "approved_amount": approved_amount,
    }

    return render(
        request,
        "adminpanel/withdraw_requests.html",
        context
    )


# =========================================================
# APPROVE WITHDRAWAL
# =========================================================

@login_required
@transaction.atomic
def approve_withdraw(request, withdraw_id):
    withdraw = get_object_or_404(
        WithdrawRequest,
        id=withdraw_id
    )

    if withdraw.status != "Pending":
        messages.warning(
            request,
            "This withdrawal request has already been processed."
        )

        return redirect("withdraw_requests")

    wallet = get_object_or_404(
        Wallet,
        user=withdraw.user
    )

    # Check balance
    if withdraw.amount > wallet.balance:
        withdraw.status = "Rejected"
        withdraw.admin_remark = (
            "Insufficient wallet balance."
        )
        withdraw.approved_by = request.user
        withdraw.approved_at = timezone.now()
        withdraw.save()

        # User notification
        Notification.objects.create(
            user=withdraw.user,
            message=(
                f"Your withdrawal request of "
                f"MMK {withdraw.amount:,.0f} "
                f"was rejected because of "
                f"insufficient wallet balance."
            ),
            notification_type="withdraw_rejected",
        )

        # ADMIN RECENT ACTIVITY
        AdminActivity.objects.create(
            admin=request.user,
            action="reject_withdraw",
            message=(
                f"You successfully rejected a withdrawal "
                f"of MMK {withdraw.amount:,.0f} "
                f"from {withdraw.user.username} "
                f"because of insufficient balance"
            )
        )

        messages.error(
            request,
            "Withdrawal rejected because of insufficient balance."
        )

        return redirect("withdraw_requests")

        # Deduct balance
    wallet.balance -= withdraw.amount
    wallet.save()

    # Update withdrawal
    withdraw.status = "Approved"
    withdraw.approved_at = timezone.now()
    withdraw.approved_by = request.user
    withdraw.save()

    # Transaction history
    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Withdraw",
        amount=withdraw.amount,
        status="Approved",
        description="Withdrawal approved by admin",
        reference_id=str(withdraw.id),
    )

    # User notification
    Notification.objects.create(
        user=withdraw.user,
        message=(
            f"Your withdrawal request of "
            f"MMK {withdraw.amount:,.0f} "
            f"has been approved."
        ),
        notification_type="withdraw_approved",
    )

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="approve_withdraw",
        message=(
            f"You successfully approved a withdrawal "
            f"of MMK {withdraw.amount:,.0f} "
            f"for {withdraw.user.username}"
        )
    )

    messages.success(
        request,
        "Withdrawal approved successfully."
    )

    return redirect("withdraw_requests")


# =========================================================
# REJECT WITHDRAWAL
# =========================================================

@login_required
@transaction.atomic
def reject_withdraw(request, withdraw_id):
    withdraw = get_object_or_404(
        WithdrawRequest,
        id=withdraw_id
    )

    if withdraw.status != "Pending":
        messages.warning(
            request,
            "This withdrawal request has already been processed."
        )

        return redirect("withdraw_requests")

    withdraw.status = "Rejected"
    withdraw.approved_by = request.user
    withdraw.approved_at = timezone.now()
    withdraw.save()

    # User notification
    Notification.objects.create(
        user=withdraw.user,
        message=(
            f"Your withdrawal request of "
            f"MMK {withdraw.amount:,.0f} "
            f"was rejected."
        ),
        notification_type="withdraw_rejected",
    )

    # ADMIN RECENT ACTIVITY
    AdminActivity.objects.create(
        admin=request.user,
        action="reject_withdraw",
        message=(
            f"You successfully rejected a withdrawal "
            f"of MMK {withdraw.amount:,.0f} "
            f"from {withdraw.user.username}"
        )
    )

    messages.success(
        request,
        "Withdrawal rejected successfully."
    )

    return redirect("withdraw_requests")


# =========================================================
# READ NOTIFICATION
# =========================================================

@login_required
def read_notification(request, noti_id):
    notification = get_object_or_404(
        Notification,
        id=noti_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("dashboard")


# =========================================================
# ORDERS - ALL STATUS
# =========================================================

@login_required
def orders(request):
    """View all orders with status filter"""
    status_filter = request.GET.get('status', 'all')

    orders = Order.objects.select_related(
        'user__user', 'seller__user'
    ).prefetch_related('items').order_by('-created_at')

    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    # Count by status
    pending_orders = Order.objects.filter(status='pending')
    ready_orders = Order.objects.filter(status='ready_for_pickup')
    picked_up_orders = Order.objects.filter(status='picked_up')
    completed_orders = Order.objects.filter(status='completed')
    cancelled_orders = Order.objects.filter(status='cancelled')

    context = {
        'orders': orders,
        'current_status': status_filter,
        'pending_orders': pending_orders,
        'ready_orders': ready_orders,
        'picked_up_orders': picked_up_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'pending_count': pending_orders.count(),
        'ready_count': ready_orders.count(),
        'picked_up_count': picked_up_orders.count(),
        'completed_count': completed_orders.count(),
        'cancelled_count': cancelled_orders.count(),
        'total_orders': Order.objects.count(),
    }

    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# PENDING ORDERS
# =========================================================

@login_required
def pending_orders(request):
    orders = Order.objects.filter(
        status='pending'
    ).select_related('user__user', 'seller__user').order_by('-created_at')

    context = {
        'orders': orders,
        'title': 'Pending Orders',
        'status': 'pending',
    }
    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# READY FOR PICKUP ORDERS
# =========================================================

@login_required
def ready_for_pickup_orders(request):
    orders = Order.objects.filter(
        status='ready_for_pickup'
    ).select_related('user__user', 'seller__user').order_by('-ready_for_pickup_at')

    context = {
        'orders': orders,
        'title': 'Ready for Pickup Orders',
        'status': 'ready_for_pickup',
    }
    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# PICKED UP ORDERS
# =========================================================

@login_required
def picked_up_orders(request):
    orders = Order.objects.filter(
        status='picked_up'
    ).select_related('user__user', 'seller__user').order_by('-picked_up_at')

    context = {
        'orders': orders,
        'title': 'Picked Up Orders',
        'status': 'picked_up',
    }
    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# COMPLETED ORDERS
# =========================================================

@login_required
def completed_orders(request):
    orders = Order.objects.filter(
        status='completed'
    ).select_related('user__user', 'seller__user').order_by('-completed_at')

    context = {
        'orders': orders,
        'title': 'Completed Orders',
        'status': 'completed',
    }
    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# CANCELLED ORDERS
# =========================================================

@login_required
def cancelled_orders(request):
    orders = Order.objects.filter(
        status='cancelled'
    ).select_related('user__user', 'seller__user').order_by('-cancelled_at')

    context = {
        'orders': orders,
        'title': 'Cancelled Orders',
        'status': 'cancelled',
    }
    return render(request, 'adminpanel/orders.html', context)


# =========================================================
# ORDER DETAIL
# =========================================================

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('user__user', 'seller__user').prefetch_related(
            'items__item__images', 'items__size_variant'
        ),
        id=order_id
    )

    context = {
        'order': order,
    }

    return render(request, 'adminpanel/order_detail.html', context)


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)

    try:
        if new_status == 'ready_for_pickup':
            if order.status == 'pending':
                order.mark_ready_for_pickup()
                messages.success(request, f"Order #{order.id} marked as ready for pickup")
            else:
                messages.error(request, "Only pending orders can be marked as ready")

        elif new_status == 'picked_up':
            if order.status == 'ready_for_pickup':
                order.mark_picked_up()
                messages.success(request, f"Order #{order.id} marked as picked up")
            else:
                messages.error(request, "Only ready for pickup orders can be marked as picked up")

        elif new_status == 'completed':
            if order.status == 'picked_up':
                order.mark_completed()
                messages.success(request, f"Order #{order.id} completed. Payment released.")
            else:
                messages.error(request, "Only picked up orders can be completed")

        elif new_status == 'cancelled':
            if order.can_cancel:
                order.cancel_order("Cancelled by admin")
                messages.success(request, f"Order #{order.id} cancelled. Refund processed.")
            else:
                messages.error(request, "Order cannot be cancelled")
        else:
            messages.error(request, "Invalid status")

    except ValueError as e:
        messages.error(request, str(e))

    return redirect('admin_order_detail', order_id=order.id)