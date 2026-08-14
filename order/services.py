# order/services.py

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart, CartItem
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem


class OrderService:
    CANCELLATION_WINDOW_MINUTES = 30  # Configurable
    MAX_CANCELLATIONS_PER_MONTH = 3

    @classmethod
    @transaction.atomic
    def create_orders_from_cart(cls, cart, user_profile):
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
        cancel_deadline = timezone.now() + timedelta(minutes=cls.CANCELLATION_WINDOW_MINUTES)

        for seller, items in items_by_seller.items():
            # Calculate seller total
            seller_total = sum(item.line_total for item in items)

            # Create order
            order = Order.objects.create(
                user=user_profile,
                seller=seller,
                cart=cart,
                total_amount=seller_total,
                status='pending',
                payment_status='held',
                pending_at=timezone.now(),
                cancel_deadline=cancel_deadline
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
        """Mark order as picked up (buyer confirms pickup)"""
        order = Order.objects.select_for_update().get(id=order_id)

        # Can be confirmed by either buyer or seller
        if order.user != user_profile and order.seller != user_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_picked_up()
        return order

    @classmethod
    @transaction.atomic
    def mark_order_completed(cls, order_id, seller_profile):
        """Mark order as completed and release funds"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.seller != seller_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_completed()
        return order