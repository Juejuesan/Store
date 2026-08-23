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
from django.core.paginator import Paginator



# =========================================================
# AUTO READY EXPIRED ORDERS
# =========================================================

def check_and_auto_ready_orders():
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
    """Display all orders belonging to the current buyer."""

    # Auto ready expired orders
    check_and_auto_ready_orders()

    # Status filter
    status_filter = request.GET.get("status", "all")

    # Get orders
    orders = (
        Order.objects
        .filter(user=request.user.profile)
        .select_related("seller__user")
        .prefetch_related("items__item__images")
        .order_by("-created_at")
    )

    # Apply filter
    if status_filter != "all":
        orders = orders.filter(status=status_filter)

    # Pagination - 10 orders per page
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Context
    context = {
        "orders": page_obj,
        "page_obj": page_obj,
        "is_buyer_view": True,
        "current_status": status_filter,
    }

    return render(request, "order_list.html", context)

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
    # AUTO-READY THIS ORDER IF EXPIRED
    # -----------------------------------------------------

    if (
        order.status == 'pending'
        and order.auto_ready_at
        and timezone.now() >= order.auto_ready_at
        and order.seller_confirmed
    ):
        order.mark_ready_for_pickup()
        order.refresh_from_db()

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
        return redirect("order:order_list")

    # -----------------------------------------------------
    # CANCELLATION INFO (ONLY FOR BUYER)
    # -----------------------------------------------------

    cancellation_count = 0
    max_cancellations = 3
    can_cancel_more = True

    if order.user == request.user.profile:
        # Count THIS user's cancellations only
        cancellation_count = Order.get_user_cancellation_count_this_month(
            request.user.profile
        )
        can_cancel_more = cancellation_count < max_cancellations

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
        "cancellation_count": cancellation_count,
        "max_cancellations": max_cancellations,
        "can_cancel_more": can_cancel_more,
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

from django.core.paginator import Paginator
from django.db.models import Sum

@login_required
def sale_list(request):
    """
    Display all sales belonging to the current seller.
    """

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    status_filter = request.GET.get("status", "all")

    # -----------------------------------------------------
    # GET SALES
    # -----------------------------------------------------

    sales = (
        Order.objects
        .filter(seller=request.user.profile)
        .order_by("-created_at")
    )

    # Apply status filter
    if status_filter != "all":
        sales = sales.filter(status=status_filter)

    # -----------------------------------------------------
    # TOTAL EARNED (released payments)
    # -----------------------------------------------------

    total_earned = (
        Order.objects
        .filter(
            seller=request.user.profile,
            payment_status="released"
        )
        .aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0
    )

    # -----------------------------------------------------
    # PENDING AMOUNT (ready_for_pickup status)
    # -----------------------------------------------------

    pending_amount = (
        Order.objects
        .filter(
            seller=request.user.profile,
            status="ready_for_pickup"
        )
        .aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0
    )

    # -----------------------------------------------------
    # STATUS COUNTS
    # -----------------------------------------------------

    pending_count = Order.objects.filter(
        seller=request.user.profile,
        status="pending"
    ).count()

    ready_count = Order.objects.filter(
        seller=request.user.profile,
        status="ready_for_pickup"
    ).count()

    completed_count = Order.objects.filter(
        seller=request.user.profile,
        status__in=["picked_up", "completed"]
    ).count()

    cancelled_count = Order.objects.filter(
        seller=request.user.profile,
        status="cancelled"
    ).count()

    # -----------------------------------------------------
    # PAGINATION (10 per page)
    # -----------------------------------------------------

    paginator = Paginator(sales, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "sales": page_obj,
        "page_obj": page_obj,
        "current_status": status_filter,
        "total_earned": total_earned,
        "pending_amount": pending_amount,
        "pending_count": pending_count,
        "ready_count": ready_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
        "total_sales": Order.objects.filter(seller=request.user.profile).count(),
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

# =========================================================
# SELLER CONFIRM PICKUP DETAILS
# =========================================================

@login_required
def confirm_seller_pickup(request, order_id):
    """
    Seller confirms their pickup location and phone number.
    Order will only auto-ready when BOTH:
    1. Seller confirms details
    2. Countdown finishes
    """

    # -----------------------------------------------------
    # GET ORDER
    # -----------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id,
        seller=request.user.profile,
        status="pending"
    )

    # -----------------------------------------------------
    # HANDLE FORM SUBMISSION
    # -----------------------------------------------------

    if request.method == "POST":

        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "").strip()

        # -------------------------------------------------
        # VALIDATE PHONE
        # -------------------------------------------------

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("order:confirm_seller_pickup", order_id=order.id)

        if not phone.isdigit():
            messages.error(request, "Phone number must contain only numbers.")
            return redirect("order:confirm_seller_pickup", order_id=order.id)

        if len(phone) < 10 or len(phone) > 11:
            messages.error(request, "Phone number must be 10-11 digits.")
            return redirect("order:confirm_seller_pickup", order_id=order.id)

        # -------------------------------------------------
        # VALIDATE LOCATION
        # -------------------------------------------------

        if not location:
            messages.error(request, "Pickup location is required.")
            return redirect("order:confirm_seller_pickup", order_id=order.id)

        # -------------------------------------------------
        # SAVE CONFIRMATION
        # -------------------------------------------------

        try:
            order.confirm_seller_details(phone, location)
            messages.success(
                request,
                "Pickup details confirmed! Our team will contact you soon."
            )
            return redirect("order:order_detail", order_id=order.id)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("order:confirm_seller_pickup", order_id=order.id)

    # -----------------------------------------------------
    # DISPLAY FORM
    # -----------------------------------------------------

    context = {
        "order": order,
    }

    return render(request, "confirm_seller_pickup.html", context)