from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from .models import Cart, CartItem, StockHold
from posts.models import Item, SizeVariant


@login_required
def view_cart(request):
    """Display cart with items and their hold status"""
    profile = request.user.profile
    cart = Cart.objects.filter(user=profile, status='open').first()

    if not cart:
        cart = Cart.objects.create(user=profile)

    # Release expired holds
    cart_items = cart.lines.filter(status='taken')

    for item in cart_items:
        hold = item.active_hold
        if hold and hold.is_expired:
            hold.release_if_expired()

    # Refresh items after releasing expired
    cart_items = cart.lines.filter(status='taken')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'now': timezone.now(),
    }
    return render(request, 'cart.html', context)  # Changed from 'cart/cart.html' to 'cart.html'


@login_required
def add_to_cart(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        profile = request.user.profile
        size_variant_id = request.POST.get('size_variant_id')
        quantity = int(request.POST.get('quantity', 1))

        cart, created = Cart.objects.get_or_create(
            user=profile,
            status='open'
        )

        with transaction.atomic():
            item = Item.objects.get(id=item_id)
            size_variant = None

            if item.has_sizes:
                if size_variant_id:
                    size_variant = SizeVariant.objects.get(id=size_variant_id)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please select a size'
                    })

            if size_variant:
                unit_price = size_variant.price

                # CHECK STOCK
                if size_variant.quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'message': f'Insufficient stock. Only {size_variant.quantity} available'
                    })

                # REDUCE STOCK
                size_variant.quantity -= quantity
                size_variant.save()

            else:
                unit_price = item.price

                # CHECK STOCK
                if item.simple_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'message': f'Insufficient stock. Only {item.simple_quantity} available'
                    })

                # REDUCE STOCK
                item.simple_quantity -= quantity
                item.save(skip_has_sizes=True)

            # CREATE CART ITEM
            cart_item = CartItem(
                cart=cart,
                item=item,
                size_variant=size_variant,
                unit_price=unit_price,
                quantity=quantity,
                item_name=item.name,
                status='taken'
            )

            cart_item.save()
            cart_item.create_hold()

            return JsonResponse({
                'success': True,
                'message': 'Added to cart successfully!',
                'cart_count': cart.total_items()
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@login_required
def update_cart_item(request, cart_item_id):
    """Update quantity of cart item"""
    if request.method != 'POST':
        return redirect('cart:view_cart')  # FIXED

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    new_quantity = int(request.POST.get('quantity', 1))

    try:
        with transaction.atomic():
            # Check if new quantity is valid
            if new_quantity <= 0:
                # Remove item
                cart_item.release_hold()
                cart_item.status = 'cancelled'
                cart_item.save()
                messages.success(request, "Item removed from cart")
                return redirect('cart:view_cart')  # FIXED

            # Check available stock for new quantity
            available = cart_item.get_available_stock()
            if available + cart_item.quantity < new_quantity:
                messages.error(request, f"Insufficient stock. Only {available + cart_item.quantity} available")
                return redirect('cart:view_cart')  # FIXED

            # Update quantity
            old_quantity = cart_item.quantity
            cart_item.quantity = new_quantity
            cart_item.save()

            # Update hold quantity (keep same expiry)
            hold = cart_item.active_hold
            if hold:
                hold.quantity = new_quantity
                hold.save()

            messages.success(request, f"Quantity updated to {new_quantity}")

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect('cart:view_cart')  # FIXED


@login_required
def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    if request.method != 'POST':
        return redirect('cart:view_cart')  # FIXED

    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    try:
        with transaction.atomic():
            cart_item.release_hold()
            cart_item.status = 'cancelled'
            cart_item.save()
            messages.success(request, "Item removed from cart")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect('cart:view_cart')  # FIXED


@login_required
def checkout(request):
    """Process checkout and purchase items"""
    profile = request.user.profile
    cart = Cart.objects.filter(user=profile, status='open').first()

    if not cart:
        messages.error(request, "No active cart")
        return redirect('cart:view_cart')  # FIXED

    try:
        with transaction.atomic():
            # Get all taken items
            cart_items = cart.lines.filter(status='taken')

            if not cart_items.exists():
                messages.error(request, "Cart is empty")
                return redirect('cart:view_cart')  # FIXED

            # Check all holds are still valid
            for item in cart_items:
                hold = item.active_hold
                if not hold or hold.is_expired:
                    item.release_hold()
                    messages.error(request, f"{item.item_name} has expired")
                    return redirect('cart:view_cart')  # FIXED

            # Calculate total
            total = sum(item.line_total for item in cart_items)

            # Check wallet balance (adjust based on your wallet implementation)
            if hasattr(profile, 'wallet'):
                if profile.wallet.balance < total:
                    messages.error(request, f"Insufficient balance. Need {total}, have {profile.wallet.balance}")
                    return redirect('cart:view_cart')  # FIXED

                # Deduct from wallet
                profile.wallet.balance -= total
                profile.wallet.save()
            else:
                messages.error(request, "Wallet not found")
                return redirect('cart:view_cart')  # FIXED

            # Consume all holds (purchase items)
            for item in cart_items:
                item.consume_hold()

            # Mark cart as checked out
            cart.status = 'checked_out'
            cart.save()

            messages.success(request, f"Purchase successful! Total: {total} MMK")
            return redirect('cart:view_cart')  # FIXED (change to order confirmation if you have one)

    except Exception as e:
        messages.error(request, f"Checkout error: {str(e)}")

    return redirect('cart:view_cart')  # FIXED


@login_required
def cart_count(request):
    """Return cart count for navbar badge"""
    profile = request.user.profile
    cart = Cart.objects.filter(user=profile, status='open').first()

    if cart:
        count = cart.total_items()
    else:
        count = 0

    return JsonResponse({'cart_count': count})