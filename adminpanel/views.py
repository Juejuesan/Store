from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from order.models import Order

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

    recent_activities = (
        AdminActivity.objects
        .select_related("admin")
        .order_by("-created_at")[:10]
    )

    context = {
        "total_users": User.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True,
        ).count(),

        "total_sellers": User.objects.filter(
            is_staff=False,
            is_superuser=False,
        ).count(),

        "pending_posts": Post.objects.filter(
            status="pending"
        ).count(),

        "pending_orders": Order.objects.filter(
            status="pending"
        ).count(),

        "total_revenue": (
            Order.objects
            .filter(status="completed")
            .aggregate(total=Sum("total_amount"))["total"]
            or Decimal("0")
        ),

        "recent_activities": recent_activities,
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
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
            is_superuser=False,
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
        context,
    )


# =========================================================
# BAN USER
# =========================================================

@login_required
def ban_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    profile = get_object_or_404(
        Profile,
        user=user,
    )

    profile.status = "Banned"
    profile.save()

    AdminActivity.objects.create(
        admin=request.user,
        action="ban_user",
        message=(
            f"You successfully banned "
            f"{user.username}"
        ),
    )

    messages.success(
        request,
        f"{user.username} has been banned successfully.",
    )

    return redirect("users")


# =========================================================
# UNBAN USER
# =========================================================

@login_required
def unban_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    profile = get_object_or_404(
        Profile,
        user=user,
    )

    profile.status = "Approved"
    profile.save()

    AdminActivity.objects.create(
        admin=request.user,
        action="unban_user",
        message=(
            f"You successfully unbanned "
            f"{user.username}"
        ),
    )

    messages.success(
        request,
        f"{user.username} has been unbanned successfully.",
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
        },
    )


# =========================================================
# POST DETAIL
# =========================================================

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


# =========================================================
# APPROVE POST
# =========================================================

@login_required
def approve_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    post.status = "approved"
    post.save()

    try:
        username = post.user.user.username
    except AttributeError:
        username = "user"

    AdminActivity.objects.create(
        admin=request.user,
        action="approve_post",
        message=(
            f"You successfully approved "
            f"a post from {username}"
        ),
    )

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been approved.",
        notification_type="approved",
    )

    messages.success(
        request,
        "Post approved successfully.",
    )

    return redirect("posts")


# =========================================================
# REJECT POST
# =========================================================

@login_required
def reject_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    post.status = "rejected"
    post.save()

    try:
        username = post.user.user.username
    except AttributeError:
        username = "user"

    AdminActivity.objects.create(
        admin=request.user,
        action="reject_post",
        message=(
            f"You successfully rejected "
            f"a post from {username}"
        ),
    )

    Notification.objects.create(
        user=post.user.user,
        post=post,
        message="Your post has been rejected.",
        notification_type="rejected",
    )

    messages.success(
        request,
        "Post rejected successfully.",
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
        context,
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
        context,
    )


# =========================================================
# APPROVE DEPOSIT
# =========================================================

@login_required
@transaction.atomic
def approve_deposit(request, deposit_id):

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id,
    )

    if deposit.status != "Pending":

        messages.warning(
            request,
            "This deposit request has already been processed.",
        )

        return redirect("deposit_requests")

    wallet, created = Wallet.objects.get_or_create(
        user=deposit.user,
    )

    wallet.balance += deposit.amount
    wallet.save()

    deposit.status = "Approved"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Deposit",
        amount=deposit.amount,
        status="Approved",
        description="Deposit approved by admin",
        reference_id=str(deposit.id),
    )

    Notification.objects.create(
        user=deposit.user,
        message=(
            f"Your deposit of "
            f"MMK {deposit.amount:,.0f} "
            f"has been approved."
        ),
        notification_type="deposit_approved",
    )

    AdminActivity.objects.create(
        admin=request.user,
        action="approve_deposit",
        message=(
            f"You successfully approved a deposit "
            f"of MMK {deposit.amount:,.0f} "
            f"from {deposit.user.username}"
        ),
    )

    messages.success(
        request,
        "Deposit approved successfully.",
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
        id=deposit_id,
    )

    if deposit.status != "Pending":

        messages.warning(
            request,
            "This deposit request has already been processed.",
        )

        return redirect("deposit_requests")

    deposit.status = "Rejected"
    deposit.approved_at = timezone.now()
    deposit.approved_by = request.user
    deposit.save()

    Notification.objects.create(
        user=deposit.user,
        message=(
            f"Your deposit request of "
            f"MMK {deposit.amount:,.0f} "
            f"was rejected."
        ),
        notification_type="deposit_rejected",
    )

    AdminActivity.objects.create(
        admin=request.user,
        action="reject_deposit",
        message=(
            f"You successfully rejected a deposit "
            f"of MMK {deposit.amount:,.0f} "
            f"from {deposit.user.username}"
        ),
    )

    messages.success(
        request,
        "Deposit rejected successfully.",
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
        "adminpanel/wallet.html",
        context,
    )


# =========================================================
# APPROVE WITHDRAWAL
# =========================================================

@login_required
@transaction.atomic
def approve_withdraw(request, withdraw_id):

    withdraw = get_object_or_404(
        WithdrawRequest,
        id=withdraw_id,
    )

    if withdraw.status != "Pending":

        messages.warning(
            request,
            "This withdrawal request has already been processed.",
        )

        return redirect("withdraw_requests")

    wallet = get_object_or_404(
        Wallet,
        user=withdraw.user,
    )

    if withdraw.amount > wallet.balance:

        withdraw.status = "Rejected"
        withdraw.admin_remark = (
            "Insufficient wallet balance."
        )
        withdraw.approved_by = request.user
        withdraw.approved_at = timezone.now()
        withdraw.save()

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

        AdminActivity.objects.create(
            admin=request.user,
            action="reject_withdraw",
            message=(
                f"You successfully rejected a withdrawal "
                f"of MMK {withdraw.amount:,.0f} "
                f"from {withdraw.user.username} "
                f"because of insufficient balance"
            ),
        )

        messages.error(
            request,
            "Withdrawal rejected because of insufficient balance.",
        )

        return redirect("withdraw_requests")

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
        reference_id=str(withdraw.id),
    )

    Notification.objects.create(
        user=withdraw.user,
        message=(
            f"Your withdrawal request of "
            f"MMK {withdraw.amount:,.0f} "
            f"has been approved."
        ),
        notification_type="withdraw_approved",
    )

    AdminActivity.objects.create(
        admin=request.user,
        action="approve_withdraw",
        message=(
            f"You successfully approved a withdrawal "
            f"of MMK {withdraw.amount:,.0f} "
            f"for {withdraw.user.username}"
        ),
    )

    messages.success(
        request,
        "Withdrawal approved successfully.",
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
        id=withdraw_id,
    )

    if withdraw.status != "Pending":

        messages.warning(
            request,
            "This withdrawal request has already been processed.",
        )

        return redirect("withdraw_requests")

    withdraw.status = "Rejected"
    withdraw.approved_by = request.user
    withdraw.approved_at = timezone.now()
    withdraw.save()

    Notification.objects.create(
        user=withdraw.user,
        message=(
            f"Your withdrawal request of "
            f"MMK {withdraw.amount:,.0f} "
            f"was rejected."
        ),
        notification_type="withdraw_rejected",
    )

    AdminActivity.objects.create(
        admin=request.user,
        action="reject_withdraw",
        message=(
            f"You successfully rejected a withdrawal "
            f"of MMK {withdraw.amount:,.0f} "
            f"from {withdraw.user.username}"
        ),
    )

    messages.success(
        request,
        "Withdrawal rejected successfully.",
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
        user=request.user,
    )

    notification.is_read = True
    notification.save()

    return redirect("dashboard")


# =========================================================
# AUTO READY ORDERS
# =========================================================

def check_and_auto_ready_orders():
    """
    Automatically change pending orders to
    ready_for_pickup after auto_ready_at.
    """

    now = timezone.now()

    Order.objects.filter(
        status="pending",
        auto_ready_at__isnull=False,
        auto_ready_at__lte=now,
    ).update(
        status="ready_for_pickup",
        ready_for_pickup_at=now,
        updated_at=now,
    )


# =========================================================
# ALL ORDERS
# =========================================================

@login_required
def orders(request):
    """
    Display all orders with status counts.
    """

    # Check expired 24-hour orders first.
    check_and_auto_ready_orders()

    orders_queryset = (
        Order.objects
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-created_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "all",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# PENDING ORDERS
# =========================================================

@login_required
def pending_orders(request):
    """
    Display pending orders.
    """

    check_and_auto_ready_orders()

    orders_queryset = (
        Order.objects
        .filter(status="pending")
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-created_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "pending",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# READY FOR PICKUP ORDERS
# =========================================================

@login_required
def ready_for_pickup_orders(request):
    """
    Display orders ready for pickup.
    """

    orders_queryset = (
        Order.objects
        .filter(status="ready_for_pickup")
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-ready_for_pickup_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "ready_for_pickup",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# PICKED UP ORDERS
# =========================================================

@login_required
def picked_up_orders(request):
    """
    Display picked-up orders.
    """

    orders_queryset = (
        Order.objects
        .filter(status="picked_up")
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-picked_up_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "picked_up",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# COMPLETED ORDERS
# =========================================================

@login_required
def completed_orders(request):
    """
    Display completed orders.
    """

    orders_queryset = (
        Order.objects
        .filter(status="completed")
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-completed_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "completed",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# CANCELLED ORDERS
# =========================================================

@login_required
def cancelled_orders(request):
    """
    Display cancelled orders.
    """

    orders_queryset = (
        Order.objects
        .filter(status="cancelled")
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related("items")
        .order_by("-cancelled_at")
    )

    context = {
        "orders": orders_queryset,
        "current_status": "cancelled",

        "pending_count": Order.objects.filter(
            status="pending"
        ).count(),

        "ready_count": Order.objects.filter(
            status="ready_for_pickup"
        ).count(),

        "picked_up_count": Order.objects.filter(
            status="picked_up"
        ).count(),

        "completed_count": Order.objects.filter(
            status="completed"
        ).count(),

        "cancelled_count": Order.objects.filter(
            status="cancelled"
        ).count(),

        "total_orders": Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/orders.html",
        context,
    )


# =========================================================
# ORDER DETAIL
# =========================================================

@login_required
def order_detail(request, order_id):
    """
    Display complete order details.
    """

    order = get_object_or_404(
        Order.objects
        .select_related(
            "user__user",
            "seller__user",
        )
        .prefetch_related(
            "items__item__images",
            "items__size_variant",
        ),
        id=order_id,
    )

    # Automatically move expired pending order
    # to ready_for_pickup.
    if (
        order.status == "pending"
        and order.auto_ready_at
        and timezone.now() >= order.auto_ready_at
    ):
        order.mark_ready_for_pickup()
        order.refresh_from_db()

    return render(
        request,
        "adminpanel/order_detail.html",
        {
            "order": order,
        },
    )


# =========================================================
# AUTO READY ORDER - AJAX
# =========================================================

@login_required
def auto_ready_order(request, order_id):
    """
    Check whether an order's automatic ready time
    has expired.
    """

    order = get_object_or_404(
        Order,
        id=order_id,
    )

    if (
        order.status == "pending"
        and order.auto_ready_at
        and timezone.now() >= order.auto_ready_at
    ):

        order.mark_ready_for_pickup()

        return JsonResponse({
            "success": True,
            "message": (
                "Order marked as ready for pickup"
            ),
        })

    return JsonResponse({
        "success": False,
        "message": "Order not ready yet",
    })


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@login_required
def update_order_status(request, order_id, new_status):
    """
    Update order status from admin panel.
    """

    order = get_object_or_404(
        Order.objects.select_related(
            "user__user",
            "seller__user",
        ),
        id=order_id,
    )

    try:

        # =================================================
        # READY FOR PICKUP
        # =================================================

        if new_status == "ready_for_pickup":

            if order.status != "pending":

                messages.error(
                    request,
                    (
                        "Only pending orders can be "
                        "marked as ready for pickup."
                    ),
                )

                return redirect(
                    "admin_order_detail",
                    order_id=order.id,
                )

            order.mark_ready_for_pickup()

            Notification.objects.create(
                user=order.user.user,
                message=(
                    "Your order is ready for pickup."
                ),
                notification_type="order_ready",
                target_url=f"/orders/{order.id}/",
            )

            messages.success(
                request,
                "Order marked as ready for pickup.",
            )


        # =================================================
        # PICKED UP
        # PAYMENT RELEASED TO SELLER
        # =================================================

        elif new_status == "picked_up":
            order.mark_picked_up()

            AdminActivity.objects.create(
                admin=request.user,
                action="picked_up_order",
                message=(
                    f"You marked Order as picked up "
                    f"and transferred MMK {order.total_amount:,.0f} to the seller."
                )
            )

            if order.status != "ready_for_pickup":

                messages.error(
                    request,
                    (
                        "Only ready for pickup orders "
                        "can be marked as picked up."
                    ),
                )

                return redirect(
                    "admin_order_detail",
                    order_id=order.id,
                )

            order.mark_picked_up()

            # =================================================
            # ADMIN RECENT ACTIVITY
            # =================================================

            AdminActivity.objects.create(
                admin=request.user,
                action="picked_up_order",
                message=(
                    f"You marked Order #{order.id} as picked up "
                    f"and transferred MMK {order.total_amount:,.0f} to the seller."
                )
            )

            # Buyer notification
            Notification.objects.create(
                user=order.user.user,
                message=(
                    f"Picked Up & Paid • "
                    f"MMK {order.total_amount:,.0f} "
                    f"has been paid from your wallet."
                ),
                notification_type="order_picked_up",
                target_url=f"/orders/{order.id}/",
            )

            # Seller notification
            Notification.objects.create(
                user=order.seller.user,
                message=(
                    f"Payment Received! "
                    f"MMK {order.total_amount:,.0f} "
                    f"has been added to your wallet "
                    f"for your sold item."
                ),
                notification_type="payment_received",
                target_url=f"/orders/{order.id}/",
            )

            messages.success(
                request,
                (
                    f"Order #{order.id} marked as picked up. "
                    f"Payment released to seller."
                ),
            )


        # =================================================
        # COMPLETED
        # =================================================

        elif new_status == "completed":

            if order.status != "picked_up":

                messages.error(
                    request,
                    (
                        "Only picked up orders can "
                        "be completed."
                    ),
                )

                return redirect(
                    "admin_order_detail",
                    order_id=order.id,
                )

            order.mark_completed()

            AdminActivity.objects.create(
                admin=request.user,
                action="complete_order",
                message=(
                    f"You completed delivery for order"
                )
            )

            Notification.objects.create(
                user=order.user.user,
                message=(
                    "Order completed successfully."
                ),
                notification_type="order_completed",
                target_url=f"/orders/{order.id}/",
            )

            messages.success(
                request,
                f"Order #{order.id} completed successfully.",
            )


        # =================================================
        # CANCELLED
        # =================================================

        elif new_status == "cancelled":

            if not order.can_cancel:

                messages.error(
                    request,
                    "Order cannot be cancelled.",
                )

                return redirect(
                    "admin_order_detail",
                    order_id=order.id,
                )

            order.cancel_order(
                "Cancelled by admin"
            )

            Notification.objects.create(
                user=order.user.user,
                message=(
                    f"Your order has been cancelled. "
                    f"MMK {order.total_amount:,.0f} "
                    f"has been refunded to your wallet."
                ),
                notification_type="order_cancelled",
                target_url=f"/orders/{order.id}/",
            )

            messages.success(
                request,
                (
                    f"Order #{order.id} cancelled. "
                    f"Refund processed."
                ),
            )


        # =================================================
        # INVALID STATUS
        # =================================================

        else:

            messages.error(
                request,
                "Invalid order status.",
            )

    except ValueError as e:

        messages.error(
            request,
            str(e),
        )

    return redirect(
        "admin_order_detail",
        order_id=order.id,
    )