# =========================================================
# ORDER VIEWS
# =========================================================

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from cart.models import Cart

from .models import Order
from .services import OrderService


# =========================================================
# AUTO READY EXPIRED ORDERS
# =========================================================

def check_and_auto_ready_orders():
    """
    Automatically change expired pending orders
    to ready_for_pickup.

    The notification is handled inside OrderService
    so that duplicate notifications are avoided.
    """

    return OrderService.auto_ready_orders()


# =========================================================
# PURCHASE CART
# =========================================================

@login_required
@require_POST
def purchase_cart(request):
    """
    Purchase items in the active cart and create orders.
    """

    cart = Cart.objects.filter(
        user=request.user.profile,
        status="open"
    ).first()

    # -----------------------------------------------------
    # CHECK CART
    # -----------------------------------------------------

    if not cart:
        messages.error(
            request,
            "No active cart found."
        )

        return redirect("cart:view_cart")

    # -----------------------------------------------------
    # GET CUSTOMER INFORMATION
    # -----------------------------------------------------

    phone_number = request.POST.get(
        "phone_number",
        ""
    ).strip()

    location = request.POST.get(
        "location",
        ""
    ).strip()

    # -----------------------------------------------------
    # VALIDATE PHONE NUMBER
    # -----------------------------------------------------

    if not phone_number:

        messages.error(
            request,
            "Phone number is required."
        )

        return redirect("cart:view_cart")

    if not phone_number.isdigit():

        messages.error(
            request,
            "Phone number must contain only numbers."
        )

        return redirect("cart:view_cart")

    if len(phone_number) < 10 or len(phone_number) > 11:

        messages.error(
            request,
            "Phone number must be 10-11 digits."
        )

        return redirect("cart:view_cart")

    # -----------------------------------------------------
    # VALIDATE LOCATION
    # -----------------------------------------------------

    if not location:

        messages.error(
            request,
            "Pickup location is required."
        )

        return redirect("cart:view_cart")

    # -----------------------------------------------------
    # CREATE ORDER
    # -----------------------------------------------------

    try:

        orders = OrderService.create_orders_from_cart(
            cart,
            request.user.profile,
            phone_number=phone_number,
            location=location
        )

        messages.success(
            request,
            (
                f"Order placed successfully! "
                f"{len(orders)} order(s) created. "
                f"You can cancel within 24 hours."
            )
        )

        return redirect("order:order_list")

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

        return redirect("cart:view_cart")


# =========================================================
# BUYER ORDER LIST
# =========================================================

@login_required
def order_list(request):
    """
    Display all orders belonging to the current buyer.
    """

    # -----------------------------------------------------
    # AUTO READY EXPIRED ORDERS
    # -----------------------------------------------------

    check_and_auto_ready_orders()

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    status_filter = request.GET.get(
        "status",
        "all"
    )

    # -----------------------------------------------------
    # GET ORDERS
    # -----------------------------------------------------

    orders = (
        Order.objects
        .filter(
            user=request.user.profile
        )
        .select_related(
            "seller__user"
        )
        .prefetch_related(
            "items__item__images"
        )
    )

    # -----------------------------------------------------
    # APPLY FILTER
    # -----------------------------------------------------

    if status_filter != "all":

        orders = orders.filter(
            status=status_filter
        )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "orders": orders,
        "is_buyer_view": True,
        "current_status": status_filter,
    }

    return render(
        request,
        "order_list.html",
        context
    )


# =========================================================
# ORDER DETAIL
# =========================================================

@login_required
def order_detail(request, order_id):
    """
    Display order details for the buyer or seller.
    """

    # -----------------------------------------------------
    # AUTO READY EXPIRED ORDERS
    # -----------------------------------------------------

    check_and_auto_ready_orders()

    # -----------------------------------------------------
    # GET ORDER
    # -----------------------------------------------------

    order = get_object_or_404(
        (
            Order.objects
            .select_related(
                "user__user",
                "seller__user"
            )
            .prefetch_related(
                "items__item__images",
                "items__size_variant"
            )
        ),
        id=order_id
    )

    # -----------------------------------------------------
    # AUTHORIZATION
    # -----------------------------------------------------

    if (
        order.user != request.user.profile
        and
        order.seller != request.user.profile
    ):

        messages.error(
            request,
            "Unauthorized to view this order."
        )

        return redirect(
            "order:order_list"
        )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "order": order,

        "is_buyer": (
            order.user == request.user.profile
        ),

        "is_seller": (
            order.seller == request.user.profile
        ),
    }

    return render(
        request,
        "order_detail.html",
        context
    )


# =========================================================
# CANCEL ORDER
# =========================================================

@login_required
@require_POST
def cancel_order(request, order_id):
    """
    Cancel a pending order and process refund.
    """

    reason = request.POST.get(
        "reason",
        ""
    ).strip()

    try:

        OrderService.cancel_order(
            order_id,
            request.user.profile,
            reason
        )

        messages.success(
            request,
            (
                "Order cancelled successfully. "
                "Refund processed to wallet."
            )
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

    return redirect(
        "order:order_detail",
        order_id=order_id
    )


# =========================================================
# SELLER ORDER LIST
# =========================================================

@login_required
def seller_orders(request):
    """
    Display all orders belonging to the current seller.
    """

    # -----------------------------------------------------
    # AUTO READY EXPIRED ORDERS
    # -----------------------------------------------------

    check_and_auto_ready_orders()

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    status_filter = request.GET.get(
        "status",
        "all"
    )

    # -----------------------------------------------------
    # GET SELLER ORDERS
    # -----------------------------------------------------

    orders = (
        Order.objects
        .filter(
            seller=request.user.profile
        )
        .select_related(
            "user__user"
        )
        .prefetch_related(
            "items__item__images"
        )
    )

    # -----------------------------------------------------
    # APPLY FILTER
    # -----------------------------------------------------

    if status_filter != "all":

        orders = orders.filter(
            status=status_filter
        )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "orders": orders,
        "is_seller_view": True,
        "current_status": status_filter,
    }

    return render(
        request,
        "order_list.html",
        context
    )


# =========================================================
# SELLER - MARK READY FOR PICKUP
# =========================================================

@login_required
@require_POST
def mark_ready_for_pickup(request, order_id):
    """
    Seller manually marks an order as ready for pickup.
    """

    try:

        OrderService.mark_order_ready_for_pickup(
            order_id,
            request.user.profile
        )

        messages.success(
            request,
            "Order marked as ready for pickup."
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

    return redirect(
        "order:seller_orders"
    )


# =========================================================
# MARK ORDER AS PICKED UP
# =========================================================

@login_required
@require_POST
def mark_picked_up(request, order_id):
    """
    Buyer or seller confirms that the order has been picked up.
    """

    try:

        order = OrderService.mark_order_picked_up(
            order_id,
            request.user.profile
        )

        messages.success(
            request,
            (
                "Order marked as picked up. "
                "Payment released to seller."
            )
        )

        # -------------------------------------------------
        # REDIRECT BASED ON USER TYPE
        # -------------------------------------------------

        if order.user == request.user.profile:

            return redirect(
                "order:order_list"
            )

        return redirect(
            "order:seller_orders"
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

        # -------------------------------------------------
        # SAFE REDIRECT AFTER ERROR
        # -------------------------------------------------

        return redirect(
            "order:order_detail",
            order_id=order_id
        )


# =========================================================
# MARK ORDER COMPLETED
# =========================================================

@login_required
@require_POST
def mark_completed(request, order_id):
    """
    Seller marks an order as completed.
    """

    try:

        OrderService.mark_order_completed(
            order_id,
            request.user.profile
        )

        messages.success(
            request,
            "Order completed."
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

    return redirect(
        "order:seller_orders"
    )


# =========================================================
# SELLER SALES LIST
# =========================================================

@login_required
def sale_list(request):
    """
    Display all sales belonging to the current seller.
    """

    # -----------------------------------------------------
    # GET SALES
    # -----------------------------------------------------

    sales = (
        Order.objects
        .filter(
            seller=request.user.profile
        )
        .order_by(
            "-created_at"
        )
    )

    # -----------------------------------------------------
    # TOTAL EARNED
    # -----------------------------------------------------

    total_earned = (
        Order.objects
        .filter(
            seller=request.user.profile,
            payment_status="released"
        )
        .aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0
    )

    # -----------------------------------------------------
    # PENDING AMOUNT
    # -----------------------------------------------------

    pending_amount = (
        Order.objects
        .filter(
            seller=request.user.profile,
            status="pending"
        )
        .aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0
    )

    # -----------------------------------------------------
    # STATUS COUNTS
    # -----------------------------------------------------

    pending_count = sales.filter(
        status="pending"
    ).count()

    ready_count = sales.filter(
        status="ready_for_pickup"
    ).count()

    completed_count = sales.filter(
        status__in=[
            "picked_up",
            "completed"
        ]
    ).count()

    cancelled_count = sales.filter(
        status="cancelled"
    ).count()

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "sales": sales,

        "total_earned": total_earned,

        "pending_amount": pending_amount,

        "pending_count": pending_count,

        "ready_count": ready_count,

        "completed_count": completed_count,

        "cancelled_count": cancelled_count,

        "total_sales": sales.count(),
    }

    return render(
        request,
        "sale_list.html",
        context
    )


# =========================================================
# SALE DETAIL
# =========================================================

@login_required
def sale_detail(request, order_id):
    """
    Display details of a seller's order.
    """

    order = get_object_or_404(
        Order,
        id=order_id,
        seller=request.user.profile
    )

    context = {
        "order": order,
        "items": order.items.all(),
    }

    return render(
        request,
        "sale_detail.html",
        context
    )