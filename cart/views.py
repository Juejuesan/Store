# cart/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from .models import Cart, CartItem, StockHold
from posts.models import Item, SizeVariant
from wallet.models import Wallet
import json


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
    cart_items = cart.lines.filter(status='taken').select_related(
        'item', 'size_variant'
    ).prefetch_related('holds')

    # Get wallet balance
    wallet = Wallet.objects.get_or_create(user=request.user)[0]
    wallet_balance = wallet.balance

    # Calculate cart total
    cart_total = cart.subtotal() if cart else 0

    # Calculate remaining balance
    remaining_balance = wallet_balance - cart_total

    # Check if user has sufficient balance
    has_sufficient_balance = remaining_balance >= 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'wallet_balance': wallet_balance,
        'cart_total': cart_total,
        'remaining_balance': remaining_balance,
        'has_sufficient_balance': has_sufficient_balance,
        'now': timezone.now(),
    }
    return render(request, 'cart.html', context)


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
            item = Item.objects.select_for_update().get(id=item_id)
            size_variant = None

            if item.has_sizes:
                if size_variant_id:
                    size_variant = SizeVariant.objects.select_for_update().get(id=size_variant_id)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please select a size'
                    })

            # CHECK IF ITEM ALREADY EXISTS IN CART
            existing_cart_item = None

            if size_variant:
                # For sized items - check same item + same size variant
                existing_cart_item = CartItem.objects.filter(
                    cart=cart,
                    item=item,
                    size_variant=size_variant,
                    status='taken'
                ).first()
            else:
                # For non-sized items - check same item
                existing_cart_item = CartItem.objects.filter(
                    cart=cart,
                    item=item,
                    size_variant__isnull=True,
                    status='taken'
                ).first()

            # Determine unit price
            if size_variant:
                unit_price = size_variant.price
            else:
                unit_price = item.price

            # CHECK STOCK
            if size_variant:
                if size_variant.quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'message': f'Insufficient stock. Only {size_variant.quantity} available'
                    })
            else:
                if item.simple_quantity < quantity:
                    return JsonResponse({
                        'success': False,
                        'message': f'Insufficient stock. Only {item.simple_quantity} available'
                    })

            # REDUCE STOCK
            if size_variant:
                size_variant.quantity -= quantity
                size_variant.save()
            else:
                item.simple_quantity -= quantity
                item.save(skip_has_sizes=True)

            if existing_cart_item:
                # MERGE WITH EXISTING CART ITEM
                existing_cart_item.quantity += quantity
                existing_cart_item.save()

                # Update hold quantity
                hold = existing_cart_item.active_hold
                if hold:
                    hold.quantity = existing_cart_item.quantity
                    hold.save()

                return JsonResponse({
                    'success': True,
                    'message': f'Updated quantity to {existing_cart_item.quantity} in cart!',
                    'cart_count': cart.total_items(),
                    'merged': True,
                    'new_quantity': existing_cart_item.quantity
                })

            else:
                # CREATE NEW CART ITEM
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
                    'cart_count': cart.total_items(),
                    'merged': False
                })

    except Item.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Item not found'
        }, status=404)
    except SizeVariant.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Size variant not found'
        }, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@login_required
def increase_quantity(request, cart_item_id):
    """Increase quantity by 1 - AJAX enabled"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    cart_item = get_object_or_404(
        CartItem.objects.select_for_update().select_related('item', 'size_variant', 'cart'),
        id=cart_item_id
    )

    try:
        with transaction.atomic():
            # Check available stock
            if cart_item.size_variant:
                available_stock = cart_item.size_variant.quantity
            else:
                available_stock = cart_item.item.simple_quantity

            if available_stock < 1:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock. No more available'
                })

            # Update cart item quantity
            cart_item.quantity += 1
            cart_item.save()

            # Update hold quantity
            hold = cart_item.active_hold
            if hold:
                hold.quantity = cart_item.quantity
                hold.save()

            # Reduce stock from inventory
            if cart_item.size_variant:
                cart_item.size_variant.quantity -= 1
                cart_item.size_variant.save()
                new_available_stock = cart_item.size_variant.quantity
            else:
                cart_item.item.simple_quantity -= 1
                cart_item.item.save(skip_has_sizes=True)
                new_available_stock = cart_item.item.simple_quantity

            # Calculate updated cart total
            cart = cart_item.cart
            cart_total = cart.subtotal()

            # Get wallet balance for remaining calculation
            wallet = Wallet.objects.get(user=request.user)
            remaining_balance = wallet.balance - cart_total

            return JsonResponse({
                'success': True,
                'message': f'Quantity increased to {cart_item.quantity}',
                'cart_item_id': cart_item.id,
                'new_quantity': cart_item.quantity,
                'new_subtotal': cart_item.line_total,
                'cart_total': cart_total,
                'remaining_balance': remaining_balance,
                'new_available_stock': new_available_stock,
                'removed': False
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@login_required
def decrease_quantity(request, cart_item_id):
    """Decrease quantity by 1 - AJAX enabled"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    cart_item = get_object_or_404(
        CartItem.objects.select_for_update().select_related('item', 'size_variant', 'cart'),
        id=cart_item_id
    )

    try:
        with transaction.atomic():
            # If quantity becomes 0 or less, remove item
            if cart_item.quantity <= 1:
                # Remove item from cart
                cart_item.release_hold()
                cart_item.status = 'cancelled'
                cart_item.save()

                # Calculate updated cart total
                cart = cart_item.cart
                cart_total = cart.subtotal()

                # Get wallet balance
                wallet = Wallet.objects.get(user=request.user)
                remaining_balance = wallet.balance - cart_total

                # Check if AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'{cart_item.item_name} removed from cart',
                        'cart_item_id': cart_item.id,
                        'removed': True,
                        'cart_total': cart_total,
                        'remaining_balance': remaining_balance,
                        'cart_count': cart.total_items()
                    })

                # For non-AJAX requests
                messages.success(request, f'{cart_item.item_name} removed from cart')
                return redirect('cart:view_cart')

            # Update cart item quantity
            cart_item.quantity -= 1
            cart_item.save()

            # Update hold quantity
            hold = cart_item.active_hold
            if hold:
                hold.quantity = cart_item.quantity
                hold.save()

            # Return stock to inventory
            if cart_item.size_variant:
                cart_item.size_variant.quantity += 1
                cart_item.size_variant.save()
            else:
                cart_item.item.simple_quantity += 1
                cart_item.item.save(skip_has_sizes=True)

            # Calculate updated cart total
            cart = cart_item.cart
            cart_total = cart.subtotal()

            # Get wallet balance
            wallet = Wallet.objects.get(user=request.user)
            remaining_balance = wallet.balance - cart_total

            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Quantity decreased to {cart_item.quantity}',
                    'cart_item_id': cart_item.id,
                    'new_quantity': cart_item.quantity,
                    'new_subtotal': cart_item.line_total,
                    'cart_total': cart_total,
                    'remaining_balance': remaining_balance,
                    'removed': False
                })

            # For non-AJAX requests
            messages.success(request, f'Quantity decreased to {cart_item.quantity}')
            return redirect('cart:view_cart')

    except Exception as e:
        print(f"Error: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        messages.error(request, f"Error: {str(e)}")
        return redirect('cart:view_cart')


@login_required
def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    if request.method != 'POST':
        return redirect('cart:view_cart')

    cart_item = get_object_or_404(
        CartItem.objects.select_for_update().select_related('item', 'size_variant', 'cart'),
        id=cart_item_id
    )

    try:
        with transaction.atomic():
            # Release hold and return stock
            cart_item.release_hold()
            cart_item.status = 'cancelled'
            cart_item.save()

            # Calculate updated cart total
            cart = cart_item.cart
            cart_total = cart.subtotal()

            # Get wallet balance
            wallet = Wallet.objects.get(user=request.user)
            remaining_balance = wallet.balance - cart_total

            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart',
                    'cart_item_id': cart_item.id,
                    'removed': True,
                    'cart_total': cart_total,
                    'remaining_balance': remaining_balance,
                    'cart_count': cart.total_items()
                })

            messages.success(request, "Item removed from cart")
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        messages.error(request, f"Error: {str(e)}")

    return redirect('cart:view_cart')


@login_required
def checkout(request):
    """Redirect to order purchase"""
    return redirect('order:purchase_cart')


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


@login_required
def increase_quantity(request, cart_item_id):
    """Increase quantity by 1 - AJAX enabled"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    cart_item = get_object_or_404(
        CartItem.objects.select_for_update().select_related('item', 'size_variant', 'cart'),
        id=cart_item_id
    )

    try:
        with transaction.atomic():
            # Check available stock
            if cart_item.size_variant:
                available_stock = cart_item.size_variant.quantity
            else:
                available_stock = cart_item.item.simple_quantity

            if available_stock < 1:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Insufficient stock. No more available'
                    })
                messages.error(request, 'Insufficient stock. No more available')
                return redirect('cart:view_cart')

            # Update cart item quantity
            cart_item.quantity += 1
            cart_item.save()

            # Update hold quantity
            hold = cart_item.active_hold
            if hold:
                hold.quantity = cart_item.quantity
                hold.save()

            # Reduce stock from inventory
            if cart_item.size_variant:
                cart_item.size_variant.quantity -= 1
                cart_item.size_variant.save()
            else:
                cart_item.item.simple_quantity -= 1
                cart_item.item.save(skip_has_sizes=True)

            # Calculate updated cart total
            cart = cart_item.cart
            cart_total = cart.subtotal()

            # Get wallet balance for remaining calculation
            wallet = Wallet.objects.get(user=request.user)
            remaining_balance = wallet.balance - cart_total

            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Quantity increased to {cart_item.quantity}',
                    'cart_item_id': cart_item.id,
                    'new_quantity': cart_item.quantity,
                    'new_subtotal': cart_item.line_total,
                    'cart_total': cart_total,
                    'remaining_balance': remaining_balance,
                    'removed': False
                })

            # For non-AJAX requests
            messages.success(request, f'Quantity increased to {cart_item.quantity}')
            return redirect('cart:view_cart')

    except Exception as e:
        print(f"Error: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        messages.error(request, f"Error: {str(e)}")
        return redirect('cart:view_cart')
