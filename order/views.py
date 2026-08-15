# order/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from cart.models import Cart
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem
from .services import OrderService


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
            f"You can cancel within 30 minutes."
        )
        return redirect('order:order_list')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('cart:view_cart')

@login_required
def order_list(request):
    """View all orders for user (as buyer)"""
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
        messages.success(request, "Order marked as picked up")
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
    """Mark order as completed and release funds (seller action)"""
    try:
        order = OrderService.mark_order_completed(order_id, request.user.profile)
        messages.success(request, "Order completed. Payment released to your wallet.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('order:seller_orders')