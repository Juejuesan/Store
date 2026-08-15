# order/services.py

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart, CartItem
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem


class OrderService:
    CANCELLATION_WINDOW_MINUTES = 24  # Changed to 24 hours (1 day)
    MAX_CANCELLATIONS_PER_MONTH = 3
    AUTO_READY_MINUTES = 1  # Auto-ready after 24 hours

    @classmethod
    @transaction.atomic
    def create_orders_from_cart(cls, cart, user_profile, phone_number=None, location=None):
        """
        Create orders from cart items, grouping by seller
        """
        # Get all taken cart items
        cart_items = cart.lines.filter(status='taken').select_related(
            'item', 'item__post', 'size_variant'
        )

        if not cart_items.exists():
            raise ValueError("Cart is empty")

        # Calculate total amount
        total_amount = sum(item.line_total for item in cart_items)

        # Check wallet balance
        wallet = Wallet.objects.get(user=user_profile.user)
        if wallet.balance < total_amount:
            raise ValueError("Insufficient wallet balance")

        # Hold funds (debit from wallet)
        wallet.balance -= total_amount
        wallet.save()

        # Create wallet transaction for holding funds
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type='Payment',
            amount=total_amount,
            status='Approved',
            description=f"Payment held for order",
            reference_id=f"CART-{cart.id}"
        )

        # Group items by seller
        items_by_seller = {}
        for cart_item in cart_items:
            seller = cart_item.item.post.user
            if seller not in items_by_seller:
                items_by_seller[seller] = []
            items_by_seller[seller].append(cart_item)

        # Create orders for each seller
        orders = []
        # cancel_deadline = timezone.now() + timedelta(hours=cls.CANCELLATION_WINDOW_HOURS)
        # auto_ready_at = timezone.now() + timedelta(hours=cls.AUTO_READY_HOURS)

        # for minute
        cancel_deadline = timezone.now() + timedelta(minutes=cls.CANCELLATION_WINDOW_MINUTES)
        auto_ready_at = timezone.now() + timedelta(minutes=cls.AUTO_READY_MINUTES)

        for seller, items in items_by_seller.items():
            # Calculate seller total
            seller_total = sum(item.line_total for item in items)

            # Create order with phone and location
            order = Order.objects.create(
                user=user_profile,
                seller=seller,
                cart=cart,
                total_amount=seller_total,
                status='pending',
                payment_status='held',
                pending_at=timezone.now(),
                cancel_deadline=cancel_deadline,
                auto_ready_at=auto_ready_at,  # ADDED
                phone_number=phone_number or user_profile.phone_number,
                location=location or user_profile.address,
            )

            # Create order items
            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    size_variant=cart_item.size_variant,
                    cart_item=cart_item,
                    item_name=cart_item.item_name,
                    unit_price=cart_item.unit_price,
                    quantity=cart_item.quantity
                )

                # Consume stock hold
                cart_item.consume_hold()

            orders.append(order)

        # Update cart status
        cart.status = 'checked_out'
        cart.save()

        return orders

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order_id, user_profile, reason=None):
        """Cancel order and process refund"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.user != user_profile:
            raise ValueError("Unauthorized to cancel this order")

        if not order.can_cancel:
            raise ValueError("Order cannot be cancelled - cancellation window has expired")

        # Check monthly cancellation limit
        current_count = Order.get_user_cancellation_count_this_month(user_profile)
        if current_count >= cls.MAX_CANCELLATIONS_PER_MONTH:
            raise ValueError(
                f"You have reached your monthly cancellation limit "
                f"({cls.MAX_CANCELLATIONS_PER_MONTH} cancellations). "
                f"Please wait until next month."
            )

        order.cancel_order(reason)
        return order

    @classmethod
    @transaction.atomic
    def mark_order_ready_for_pickup(cls, order_id, seller_profile):
        """Mark order as ready for pickup"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.seller != seller_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_ready_for_pickup()
        return order

    @classmethod
    @transaction.atomic
    def mark_order_picked_up(cls, order_id, user_profile):
        """Mark order as picked up - releases money to seller"""
        order = Order.objects.select_for_update().get(id=order_id)

        # Can be confirmed by buyer, seller, or admin
        if order.user != user_profile and order.seller != user_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_picked_up()
        return order

    @classmethod
    @transaction.atomic
    def mark_order_completed(cls, order_id, seller_profile):
        """Mark order as completed"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.seller != seller_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_completed()
        return order

    @classmethod
    def auto_ready_orders(cls):
        """Auto-change pending orders to ready_for_pickup after 24 hours"""
        expired_orders = Order.objects.filter(
            status='pending',
            auto_ready_at__lte=timezone.now()
        )

        updated_count = 0
        for order in expired_orders:
            try:
                order.mark_ready_for_pickup()
                updated_count += 1
            except Exception as e:
                print(f"Failed to auto-ready order #{order.id}: {str(e)}")

        return updated_count