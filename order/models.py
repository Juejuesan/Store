from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from user.models import Profile
from posts.models import Item, SizeVariant
from cart.models import Cart, CartItem
from wallet.models import Wallet, WalletTransaction


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('picked_up', 'Picked Up'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('held', 'Funds Held'),
        ('released', 'Released to Seller'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='seller_orders')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)

    total_amount = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Buyer details
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    # Seller confirmation fields (NEW)
    seller_phone = models.CharField(max_length=11, blank=True, null=True)
    seller_location = models.CharField(max_length=200, blank=True, null=True)
    seller_confirmed = models.BooleanField(default=False)
    seller_confirmed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending_at = models.DateTimeField(default=timezone.now)
    ready_for_pickup_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # Cancellation window
    cancel_deadline = models.DateTimeField(null=True, blank=True)
    auto_ready_at = models.DateTimeField(null=True, blank=True)

    # Notes
    cancellation_reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.user.user.username} - {self.status}"

    @property
    def can_cancel(self):
        """Check if order can be cancelled"""
        return (
                self.status == 'pending' and
                self.cancel_deadline and
                timezone.now() <= self.cancel_deadline
        )

    @property
    def is_cancel_window_expired(self):
        """Check if cancellation window has expired"""
        return self.cancel_deadline and timezone.now() > self.cancel_deadline

    @property
    def time_until_auto_ready(self):
        """Return time remaining until auto-ready"""
        if self.status == 'pending' and self.auto_ready_at:
            remaining = self.auto_ready_at - timezone.now()
            if remaining.total_seconds() > 0:
                return remaining
        return None

    @property
    def is_auto_ready_due(self):
        """Check if order should be auto-ready now"""
        return (
                self.status == 'pending' and
                self.auto_ready_at and
                timezone.now() >= self.auto_ready_at
        )

    @property
    def can_auto_ready(self):
        """Check if BOTH conditions met for auto-ready"""
        return (
                self.status == 'pending' and
                self.auto_ready_at and
                timezone.now() >= self.auto_ready_at and
                self.seller_confirmed
        )

    @classmethod
    def get_user_cancellation_count_this_month(cls, user_profile):
        """Get number of cancellations by user in last 5 minutes (TESTING)"""
        today = timezone.now()
        time_window = today - timedelta(minutes=5)
        return cls.objects.filter(
            user=user_profile,
            status='cancelled',
            cancelled_at__gte=time_window,
            cancelled_at__lte=today
        ).count()

    @classmethod
    def can_user_cancel_more(cls, user_profile, max_cancellations=3):
        """Check if user can cancel more orders this month"""
        cancellation_count = cls.get_user_cancellation_count_this_month(user_profile)
        return cancellation_count < max_cancellations

    def clean(self):
        """Validate phone numbers"""
        if self.phone_number:
            if not self.phone_number.isdigit():
                raise ValidationError({'phone_number': 'Phone number must contain only numbers'})
            if len(self.phone_number) < 10 or len(self.phone_number) > 11:
                raise ValidationError({'phone_number': 'Phone number must be 10-11 digits'})

        if self.seller_phone:
            if not self.seller_phone.isdigit():
                raise ValidationError({'seller_phone': 'Seller phone must contain only numbers'})
            if len(self.seller_phone) < 10 or len(self.seller_phone) > 11:
                raise ValidationError({'seller_phone': 'Seller phone must be 10-11 digits'})

    def save(self, *args, **kwargs):
        """Validate before saving"""
        self.clean()
        super().save(*args, **kwargs)

    def mark_ready_for_pickup(self):
        """Mark order as ready for pickup"""
        if self.status != 'pending':
            raise ValueError("Only pending orders can be marked as ready for pickup")

        if not self.seller_confirmed:
            raise ValueError("Seller must confirm pickup details first")

        self.status = 'ready_for_pickup'
        self.ready_for_pickup_at = timezone.now()
        self.save()

    def mark_picked_up(self):
        """Mark order as picked up and release payment to seller with 10% tax."""

        if self.status != 'ready_for_pickup':
            raise ValueError("Only ready for pickup orders can be marked as picked up")

        if self.payment_status == 'released':
            raise ValueError("Payment has already been released for this order")

        self.status = 'picked_up'
        self.picked_up_at = timezone.now()
        self.payment_status = 'released'
        self.save(update_fields=['status', 'picked_up_at', 'payment_status', 'updated_at'])

        # Release held funds to seller (with 10% tax)
        self.release_funds_to_seller()

    def mark_completed(self):
        """Item delivered to buyer - order closed"""
        if self.status != 'picked_up':
            raise ValueError("Only picked up orders can be completed")

        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def cancel_order(self, reason=None, by_admin=False):
        """Cancel order and refund to buyer"""

        # For admin cancellation - allow in ready_for_pickup too
        if by_admin:
            if self.status not in ['pending', 'ready_for_pickup']:
                raise ValueError("Order cannot be cancelled")
        else:
            # For user cancellation - only in pending
            if not self.can_cancel:
                raise ValueError("Order cannot be cancelled - cancellation window has expired")

            if not self.can_user_cancel_more(self.user):
                raise ValueError("You have reached your monthly cancellation limit (3 cancellations)")

        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.payment_status = 'refunded'
        self.save()

        # Refund to buyer
        self.refund_to_buyer()

        # Release stock holds
        self.release_stock_holds()

    def confirm_seller_details(self, phone, location):
        """Seller confirms their pickup details"""
        if self.status != 'pending':
            raise ValueError("Order is not pending")

        self.seller_phone = phone
        self.seller_location = location
        self.seller_confirmed = True
        self.seller_confirmed_at = timezone.now()
        self.save()

    def release_funds_to_seller(self):
        """Release held funds to seller's wallet after 10% tax deduction."""

        TAX_PERCENTAGE = 10  # 10% platform fee

        seller_wallet = Wallet.objects.get(user=self.seller.user)

        # Calculate tax and seller payout
        tax_amount = (self.total_amount * TAX_PERCENTAGE) // 100
        seller_payout = self.total_amount - tax_amount

        # Credit seller wallet (after tax)
        seller_wallet.balance += seller_payout
        seller_wallet.save()

        # Create wallet transaction for seller
        WalletTransaction.objects.create(
            wallet=seller_wallet,
            transaction_type='Payment',
            amount=seller_payout,
            status='Approved',
            description=f"Payment received for Order #{self.id} (after 10% platform fee)",
            reference_id=f"ORDER-{self.id}"
        )

        # Optional: Create transaction for platform fee
        if tax_amount > 0:
            # You can log the tax somewhere or create a separate transaction
            WalletTransaction.objects.create(
                wallet=seller_wallet,
                transaction_type='Payment',
                amount=-tax_amount,
                status='Approved',
                description=f"Platform fee (10%) for Order #{self.id}",
                reference_id=f"ORDER-{self.id}-FEE"
            )

    def refund_to_buyer(self):
        """Refund funds to buyer's wallet"""
        buyer_wallet = Wallet.objects.get(user=self.user.user)
        buyer_wallet.balance += self.total_amount
        buyer_wallet.save()

        WalletTransaction.objects.create(
            wallet=buyer_wallet,
            transaction_type='Refund',
            amount=self.total_amount,
            status='Approved',
            description=f"Refund for cancelled Order #{self.id}",
            reference_id=f"ORDER-{self.id}-REFUND"
        )

    def release_stock_holds(self):
        """Release stock holds for cancelled order"""
        for order_item in self.items.all():
            order_item.release_stock()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, null=True, blank=True, on_delete=models.SET_NULL)
    cart_item = models.ForeignKey(CartItem, null=True, blank=True, on_delete=models.SET_NULL)

    item_name = models.CharField(max_length=255)
    unit_price = models.IntegerField(validators=[MinValueValidator(1)])
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.size_variant:
            return f"{self.item_name} - {self.size_variant.size} x{self.quantity}"
        return f"{self.item_name} x{self.quantity}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def release_stock(self):
        """Release stock back to inventory"""
        if self.size_variant:
            self.size_variant.quantity += self.quantity
            self.size_variant.save()
        else:
            self.item.simple_quantity += self.quantity
            self.item.save(skip_has_sizes=True)

        if self.cart_item:
            self.cart_item.release_hold()