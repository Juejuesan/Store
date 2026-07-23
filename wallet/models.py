from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# ==========================================================
# WALLET
# One wallet for each user
# ==========================================================

class Wallet(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} Wallet"
# ==========================================================
# DEPOSIT REQUEST
# User uploads payment screenshot
# Admin approves manually
# ==========================================================

class DepositRequest(models.Model):

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    PAYMENT_METHOD = (

        ("KBZ Pay", "KBZ Pay"),
        ("Wave Pay", "Wave Pay"),
        ("AYA Pay", "AYA Pay"),
        ("CB Pay", "CB Pay"),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deposits"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD
    )

    sender_phone = models.CharField(
        max_length=20
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    screenshot = models.ImageField(
        upload_to="deposit_ss/"
    )

    note = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    admin_remark = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_deposit_requests"
    )

    sender_name = models.CharField(
        max_length=100
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(fields=["status"]),

            models.Index(fields=["transaction_id"]),

            models.Index(fields=["created_at"]),

        ]

    def __str__(self):

        return f"Deposit #{self.id} - {self.user.username}"
# ==========================================================
# WITHDRAW REQUEST
# ==========================================================

class WithdrawRequest(models.Model):

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    PAYMENT_METHOD = (

        ("KBZ Pay", "KBZ Pay"),
        ("Wave Pay", "Wave Pay"),
        ("AYA Pay", "AYA Pay"),
        ("CB Pay", "CB Pay"),

        ("Bank Transfer", "Bank Transfer"),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdraws"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD
    )

    receiver_name = models.CharField(
        max_length=100
    )

    receiver_phone = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    note = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    admin_remark = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_withdraw_requests"
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(fields=["status"]),

            models.Index(fields=["created_at"]),

        ]

    def __str__(self):

        return f"Withdraw #{self.id} - {self.user.username}"
# ==========================================================
# WALLET HISTORY
# Every money movement is recorded forever
# ==========================================================

class WalletTransaction(models.Model):

    TRANSACTION_TYPES = (

        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
        ("Payment", "Payment"),
        ("Refund", "Refund"),

    )

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    reference_id = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.transaction_type} - {self.wallet.user.username}"