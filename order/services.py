# order/services.py

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart, CartItem
from wallet.models import Wallet, WalletTransaction
from .models import Order, OrderItem
from notifications.models import Notification

class OrderService:
    CANCELLATION_WINDOW_MINUTES = 3
    MAX_CANCELLATIONS_PER_MONTH = 3
    AUTO_READY_MINUTES = 3

    @classmethod
    @transaction.atomic
    def create_orders_from_cart(cls, cart, user_profile, phone_number=None, location=None):
        """
        Create ONE order from all cart items
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

        # Time settings
        cancel_deadline = timezone.now() + timedelta(minutes=cls.CANCELLATION_WINDOW_MINUTES)
        auto_ready_at = timezone.now() + timedelta(minutes=cls.AUTO_READY_MINUTES)

        # Get first seller (for order reference)
        first_cart_item = cart_items.first()
        seller = first_cart_item.item.post.user

        # Create ONE order for ALL items
        order = Order.objects.create(
            user=user_profile,
            seller=seller,
            cart=cart,
            total_amount=total_amount,
            status='pending',
            payment_status='held',
            pending_at=timezone.now(),
            cancel_deadline=cancel_deadline,
            auto_ready_at=auto_ready_at,
            phone_number=phone_number or user_profile.phone_number,
            location=location or user_profile.address,
            # Seller fields - ALL empty, seller will fill them
            seller_phone=None,  # Seller will provide
            seller_location=None,  # Seller will provide
            seller_confirmed=False,
        )

        # Add ALL items to the SAME order
        for cart_item in cart_items:
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

        # BUYER NOTIFICATION
        Notification.objects.create(
            user=user_profile.user,
            message="Purchase Confirmed! Admin review in progress.",
            notification_type="order_created",
            target_url=f"/orders/{order.id}/",
        )

        # SELLER NOTIFICATIONS - Ask to confirm pickup details
        unique_sellers = set(cart_item.item.post.user for cart_item in cart_items)
        for seller_profile in unique_sellers:
            Notification.objects.create(
                user=seller_profile.user,
                message=(
                    f"You received a new order (#{order.id}). "
                    f"Please confirm your pickup location and phone number."
                ),
                notification_type="order_created",
                target_url=f"/orders/{order.id}/confirm-pickup/",
            )

        # Update cart status
        cart.status = 'checked_out'
        cart.save()

        return [order]  # Return as list

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order_id, user_profile=None, reason=None, by_admin=False):
        """Cancel order and process refund."""
        order = Order.objects.select_for_update().get(id=order_id)

        if by_admin:
            # Admin can cancel pending or ready_for_pickup
            if order.status not in ['pending', 'ready_for_pickup']:
                raise ValueError("Order cannot be cancelled at this stage")
        else:
            # User cancellation - requires authorization and valid window
            if not user_profile:
                raise ValueError("User profile is required")

            if order.user != user_profile:
                raise ValueError("Unauthorized to cancel this order")

            if not order.can_cancel:
                raise ValueError("Order cannot be cancelled - cancellation window has expired")

            current_count = Order.get_user_cancellation_count_this_month(user_profile)
            if current_count >= cls.MAX_CANCELLATIONS_PER_MONTH:
                raise ValueError(
                    f"You have reached your monthly cancellation "
                    f"limit ({cls.MAX_CANCELLATIONS_PER_MONTH} "
                    f"cancellations). Please wait until next month."
                )

        order.cancel_order(reason, by_admin=by_admin)

        # BUYER NOTIFICATION
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
    def confirm_seller_pickup(cls, order_id, seller_profile, phone, location):
        """Seller confirms their pickup details (BOTH phone and location required)"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.seller != seller_profile:
            raise ValueError("Unauthorized to update this order")

        if order.status != 'pending':
            raise ValueError("Order is not pending")

        order.confirm_seller_details(phone, location)

        # Notify buyer that seller confirmed
        Notification.objects.create(
            user=order.user.user,
            message="Seller confirmed pickup details. Your order is being processed.",
            notification_type="order_updated",
            target_url=f"/orders/{order.id}/",
        )

        return order

    @classmethod
    @transaction.atomic
    def mark_order_ready_for_pickup(cls, order_id, seller_profile):
        """Mark order as ready for pickup"""
        order = Order.objects.select_for_update().get(id=order_id)

        if order.seller != seller_profile:
            raise ValueError("Unauthorized to update this order")

        order.mark_ready_for_pickup()

        Notification.objects.create(
            user=order.user.user,
            message="Your order is ready for pickup.",
            notification_type="order_ready",
            target_url=f"/orders/{order.id}/",
        )

        return order

    @classmethod
    @transaction.atomic
    def mark_order_picked_up(cls, order_id, user_profile):
        """Mark order as picked up - releases money to seller"""
        order = Order.objects.select_for_update().get(id=order_id)

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

        Notification.objects.create(
            user=order.user.user,
            message="Your order has been completed.",
            notification_type="order_completed",
            target_url=f"/orders/{order.id}/",
        )

        return order

    @classmethod
    @transaction.atomic
    def auto_ready_orders(cls):
        """Auto-ready orders where BOTH conditions are met"""
        # Countdown done AND seller confirmed
        expired_orders = Order.objects.filter(
            status="pending",
            auto_ready_at__lte=timezone.now(),
            seller_confirmed=True  # Seller must confirm first
        )

        updated_count = 0

        for order in expired_orders:
            try:
                order.mark_ready_for_pickup()

                Notification.objects.create(
                    user=order.user.user,
                    message="Your order is ready for pickup.",
                    notification_type="order_ready",
                    target_url=f"/orders/{order.id}/",
                )

                updated_count += 1

            except Exception as e:
                print(f"Failed to auto-ready order #{order.id}: {str(e)}")

        return updated_count