# order/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Q
from cart.models import Cart
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem
from .services import OrderService


def check_and_auto_ready_orders():
    """Auto-change pending orders to ready_for_pickup after 24 hours"""
    Order.objects.filter(
        status='pending',
        auto_ready_at__lte=timezone.now()
    ).update(
        status='ready_for_pickup',
        ready_for_pickup_at=timezone.now()
    )


@login_required
@require_POST
def purchase_cart(request):
    """Purchase items in cart and create orders"""
    cart = Cart.objects.filter(
        user=request.user.profile,
        status='open'
    ).first()

    if not cart:
        messages.error(request, "No active cart found")
        return redirect('cart:view_cart')

    # Get phone and location from POST data
    phone_number = request.POST.get('phone_number', '').strip()
    location = request.POST.get('location', '').strip()

    # Validate phone number
    if not phone_number:
        messages.error(request, "Phone number is required")
        return redirect('cart:view_cart')

    # Check if phone contains only digits
    if not phone_number.isdigit():
        messages.error(request, "Phone number must contain only numbers")
        return redirect('cart:view_cart')

    # Check phone length (10-11 digits)
    if len(phone_number) < 10 or len(phone_number) > 11:
        messages.error(request, "Phone number must be 10-11 digits")
        return redirect('cart:view_cart')

    # Validate location
    if not location:
        messages.error(request, "Pickup location is required")
        return redirect('cart:view_cart')

    try:
        orders = OrderService.create_orders_from_cart(
            cart,
            request.user.profile,
            phone_number=phone_number,
            location=location
        )
        messages.success(
            request,
            f"Order placed successfully! {len(orders)} order(s) created. "
            f"You can cancel within 24 hours."
        )
        return redirect('order:order_list')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('cart:view_cart')


@login_required
def order_list(request):
    """View all orders for user (as buyer)"""
    # Auto-ready expired orders
    check_and_auto_ready_orders()

    # Get filter parameter
    status_filter = request.GET.get('status', 'all')

    orders = Order.objects.filter(
        user=request.user.profile
    ).select_related('seller__user').prefetch_related('items__item__images')

    # Apply status filter
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'is_buyer_view': True,
        'current_status': status_filter
    }
    return render(request, 'order_list.html', context)


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(
        Order.objects.select_related('user__user', 'seller__user').prefetch_related(
            'items__item__images', 'items__size_variant'
        ),
        id=order_id
    )

    # Auto-ready if expired
    if order.status == 'pending' and order.auto_ready_at and timezone.now() >= order.auto_ready_at:
        order.mark_ready_for_pickup()
        order.refresh_from_db()

    # Check if user is buyer or seller
    if order.user != request.user.profile and order.seller != request.user.profile:
        messages.error(request, "Unauthorized to view this order")
        return redirect('order:order_list')

    context = {
        'order': order,
        'is_buyer': order.user == request.user.profile,
        'is_seller': order.seller == request.user.profile
    }
    return render(request, 'order_detail.html', context)


@login_required
@require_POST
def cancel_order(request, order_id):
    """Cancel pending order"""
    reason = request.POST.get('reason', '')

    try:
        order = OrderService.cancel_order(order_id, request.user.profile, reason)
        messages.success(request, "Order cancelled successfully. Refund processed to wallet.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order:order_detail', order_id=order_id)


# Seller views
@login_required
def seller_orders(request):
    """View orders for seller"""
    # Auto-ready expired orders
    check_and_auto_ready_orders()

    status_filter = request.GET.get('status', 'all')

    orders = Order.objects.filter(
        seller=request.user.profile
    ).select_related('user__user').prefetch_related('items__item__images')

    # Apply status filter
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'is_seller_view': True,
        'current_status': status_filter
    }
    return render(request, 'order_list.html', context)


@login_required
@require_POST
def mark_ready_for_pickup(request, order_id):
    """Mark order as ready for pickup (seller action)"""
    try:
        order = OrderService.mark_order_ready_for_pickup(order_id, request.user.profile)
        messages.success(request, "Order marked as ready for pickup")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order:seller_orders')


@login_required
@require_POST
def mark_picked_up(request, order_id):
    """Mark order as picked up (buyer or seller confirms)"""
    try:
        order = OrderService.mark_order_picked_up(order_id, request.user.profile)
        messages.success(request, "Order marked as picked up. Payment released to seller.")
    except ValueError as e:
        messages.error(request, str(e))

    # Redirect based on user type
    if order.user == request.user.profile:
        return redirect('order:order_list')
    else:
        return redirect('order:seller_orders')


@login_required
@require_POST
def mark_completed(request, order_id):
    """Mark order as completed"""
    try:
        order = OrderService.mark_order_completed(order_id, request.user.profile)
        messages.success(request, "Order completed.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order:seller_orders')


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from .models import Order, OrderItem


@login_required
def sale_list(request):
    # Get all orders where current user is the seller
    sales = Order.objects.filter(
        seller=request.user.profile
    ).order_by('-created_at')

    # Calculate totals
    total_earned = Order.objects.filter(
        seller=request.user.profile,
        payment_status='released'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    pending_amount = Order.objects.filter(
        seller=request.user.profile,
        status='pending'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Count by status
    pending_count = sales.filter(status='pending').count()
    ready_count = sales.filter(status='ready_for_pickup').count()
    completed_count = sales.filter(status__in=['picked_up', 'completed']).count()
    cancelled_count = sales.filter(status='cancelled').count()

    context = {
        'sales': sales,
        'total_earned': total_earned,
        'pending_amount': pending_amount,
        'pending_count': pending_count,
        'ready_count': ready_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'total_sales': sales.count(),
    }
    return render(request, 'sale_list.html', context)


@login_required
def sale_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        seller=request.user.profile
    )

    context = {
        'order': order,
        'items': order.items.all(),
    }
    return render(request, 'sale_detail.html', context)