# order/services.py

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart, CartItem
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem


class OrderService:
    CANCELLATION_WINDOW_HOURS = 24
    MAX_CANCELLATIONS_PER_MONTH = 3
    AUTO_READY_HOURS = 24


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
        cancel_deadline = timezone.now() + timedelta(
            hours=cls.CANCELLATION_WINDOW_HOURS
        )

        auto_ready_at = timezone.now() + timedelta(
            hours=cls.AUTO_READY_HOURS
        )

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
            # =========================================================
            # BUYER NOTIFICATION
            # =========================================================

            # =========================================================
            # BUYER NOTIFICATION
            # =========================================================

            Notification.objects.create(
                user=user_profile.user,
                message=(
                    "Purchase Confirmed! "
                    "Admin review in progress for item pick-up and payout."
                ),
                notification_type="order_created",
                target_url=f"/orders/{order.id}/",
            )

            # =========================================================
            # SELLER NOTIFICATION
            # =========================================================

            Notification.objects.create(
                user=seller.user,
                message="You received a new order.",
                notification_type="order_created",
                target_url=f"/orders/{order.id}/",
            )
            orders.append(order)

        # Update cart status
        cart.status = 'checked_out'
        cart.save()

        return orders

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order_id, user_profile, reason=None):
        """Cancel order and process refund."""

        order = Order.objects.select_for_update().get(
            id=order_id
        )

        # =====================================================
        # AUTHORIZATION
        # =====================================================

        if order.user != user_profile:
            raise ValueError(
                "Unauthorized to cancel this order"
            )

        # =====================================================
        # CANCELLATION WINDOW
        # =====================================================

        if not order.can_cancel:
            raise ValueError(
                "Order cannot be cancelled - "
                "cancellation window has expired"
            )

        # =====================================================
        # MONTHLY CANCELLATION LIMIT
        # =====================================================

        current_count = (
            Order.get_user_cancellation_count_this_month(
                user_profile
            )
        )

        if current_count >= cls.MAX_CANCELLATIONS_PER_MONTH:
            raise ValueError(
                f"You have reached your monthly cancellation "
                f"limit ({cls.MAX_CANCELLATIONS_PER_MONTH} "
                f"cancellations). Please wait until next month."
            )

        # =====================================================
        # CANCEL + REFUND
        # =====================================================

        order.cancel_order(reason)

        # =====================================================
        # BUYER NOTIFICATION
        # =====================================================

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

        return order

    @classmethod
    @transaction.atomic
    def mark_order_ready_for_pickup(cls, order_id, seller_profile):
        """Mark order as ready for pickup"""

        order = Order.objects.select_for_update().get(
            id=order_id
        )

        if order.seller != seller_profile:
            raise ValueError(
                "Unauthorized to update this order"
            )

        order.mark_ready_for_pickup()

        # =====================================================
        # BUYER NOTIFICATION
        # =====================================================

        Notification.objects.create(
            user=order.user.user,
            message="Your order has been picked up.",
            notification_type="order_ready",
            target_url=f"/orders/{order.id}/",
        )

        return order

    @classmethod
    @transaction.atomic
    def mark_order_completed(cls, order_id, seller_profile):
        """Mark order as completed."""

        order = Order.objects.select_for_update().get(
            id=order_id
        )

        # =====================================================
        # AUTHORIZATION
        # =====================================================

        if order.seller != seller_profile:
            raise ValueError(
                "Unauthorized to update this order"
            )

        # =====================================================
        # MARK COMPLETED
        # =====================================================

        order.mark_completed()

        # =====================================================
        # BUYER NOTIFICATION
        # =====================================================

        Notification.objects.create(
            user=order.user.user,
            message="Your order has been completed.",
            notification_type="order_completed",
            target_url=f"/orders/{order.id}/",
        )

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
    @transaction.atomic
    def auto_ready_orders(cls):
        """Auto-change expired pending orders to ready for pickup."""

        expired_orders = Order.objects.filter(
            status="pending",
            auto_ready_at__lte=timezone.now()
        )

        updated_count = 0

        for order in expired_orders:

            try:

                order.mark_ready_for_pickup()

                # =================================================
                # BUYER NOTIFICATION
                # =================================================

                Notification.objects.create(
                    user=order.user.user,
                    message="Your order is ready for pickup.",
                    notification_type="order_ready",
                    target_url=f"/orders/{order.id}/",
                )

                updated_count += 1

            except Exception as e:

                print(
                    f"Failed to auto-ready "
                    f"order #{order.id}: {str(e)}"
                )

        return updated_count