from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from user.models import Profile
from posts.models import Item, SizeVariant


class Cart(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('checked_out', 'Checked out'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return sum(line.line_total for line in self.lines.filter(status='taken'))

    def total_items(self):
        return sum(line.quantity for line in self.lines.filter(status='taken'))

    def __str__(self):
        return f"Cart {self.id} - {self.user.user.username if self.user else 'Anonymous'}"


class CartItem(models.Model):
    STATUS_CHOICES = [
        ('taken', 'Taken'),
        ('released', 'Released'),
        ('purchased', 'Purchased'),
        ('cancelled', 'Cancelled'),
    ]

    cart = models.ForeignKey(Cart, related_name='lines', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, null=True, blank=True, on_delete=models.SET_NULL)

    unit_price = models.IntegerField(validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    item_name = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='taken')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

    @property
    def line_total(self):
        if self.status == 'taken':
            return self.unit_price * self.quantity
        return 0

    @property
    def category(self):
        return self.item.post.category if self.item.post else None

    @property
    def active_hold(self):
        return self.holds.filter(status='taken').first()

    def get_available_stock(self):
        """Calculate available stock considering taken holds"""
        if self.size_variant:
            total_stock = self.size_variant.quantity
            taken_holds_query = StockHold.objects.filter(
                size_variant=self.size_variant,
                status='taken'
            )
            if self.pk:
                taken_holds_query = taken_holds_query.exclude(cart_item=self)

            taken_holds = taken_holds_query.aggregate(
                total=models.Sum('quantity')
            )['total'] or 0
            return total_stock - taken_holds
        else:
            total_stock = self.item.simple_quantity
            taken_holds_query = StockHold.objects.filter(
                item=self.item,
                size_variant__isnull=True,
                status='taken'
            )
            if self.pk:
                taken_holds_query = taken_holds_query.exclude(cart_item=self)

            taken_holds = taken_holds_query.aggregate(
                total=models.Sum('quantity')
            )['total'] or 0
            return total_stock - taken_holds

    def create_hold(self):
        """Create a stock hold for this cart item"""
        expires_at = timezone.now() + timedelta(minutes=3)
        StockHold.objects.create(
            cart_item=self,
            item=self.item,
            size_variant=self.size_variant,
            quantity=self.quantity,
            expires_at=expires_at,
            status='taken'
        )
        return expires_at

    def extend_hold(self):
        """Extend the taken hold"""
        hold = self.active_hold
        if hold:
            hold.expires_at = timezone.now() + timedelta(minutes=3)
            hold.save()
            return hold.expires_at
        return None


    def release_hold(self):
        """Release the taken hold (return stock)"""
        hold = self.active_hold
        if hold:
            hold.status = 'released'
            hold.released_at = timezone.now()
            hold.save()

            # RESTORE STOCK
            if self.size_variant:
                self.size_variant.quantity += self.quantity
                self.size_variant.save()
            else:
                self.item.simple_quantity += self.quantity
                self.item.save(skip_has_sizes=True)

            self.status = 'released'
            self.save()

    def consume_hold(self):
        """Mark hold as purchased"""
        hold = self.active_hold
        if hold:
            hold.status = 'purchased'
            hold.purchased_at = timezone.now()  # FIXED: changed from consumed_at
            hold.save()
            self.status = 'purchased'
            self.save()

    def __str__(self):
        if self.size_variant:
            return f"{self.item_name} - {self.size_variant.size} x{self.quantity}"
        return f"{self.item_name} x{self.quantity}"


class StockHold(models.Model):
    STATUS_CHOICES = [
        ('taken', 'Taken'),
        ('released', 'Released'),
        ('purchased', 'Purchased'),
    ]

    cart_item = models.ForeignKey(CartItem, related_name='holds', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, null=True, blank=True, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='taken')

    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['item', 'size_variant', 'status']),
        ]

    @property
    def is_expired(self):
        return self.status == 'taken' and self.expires_at < timezone.now()

    def release_if_expired(self):
        """Release hold if it's expired"""
        if self.is_expired:
            self.status = 'released'
            self.released_at = timezone.now()
            self.save()

            # RESTORE STOCK
            if self.size_variant:
                self.size_variant.quantity += self.quantity
                self.size_variant.save()
            else:
                self.item.simple_quantity += self.quantity
                self.item.save(skip_has_sizes=True)

            # Update cart item status
            if self.cart_item.status == 'taken':
                self.cart_item.status = 'released'
                self.cart_item.save()
            return True
        return False

    def __str__(self):
        return f"Hold for {self.item.name} - {self.quantity} units ({self.status})"