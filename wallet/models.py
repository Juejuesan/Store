from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# ==========================================================
# WALLET
# One wallet for each user
# ==========================================================

class Wallet(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet",
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00")
            )
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["created_at"]
            ),
        ]

    def __str__(self):

        return f"{self.user.username} Wallet"


# ==========================================================
# DEPOSIT REQUEST
#
# User submits:
#   - Payment method
#   - Sender information
#   - Transaction ID
#   - Amount
#   - Payment screenshot
#
# Admin manually approves/rejects the request.
# ==========================================================

class DepositRequest(models.Model):

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    # ------------------------------------------------------
    # PAYMENT METHODS
    # ------------------------------------------------------

    PAYMENT_METHOD = (

        ("KBZ Pay", "KBZ Pay"),
        ("Wave Pay", "Wave Pay"),
        ("AYA Pay", "AYA Pay"),
        ("CB Pay", "CB Pay"),

    )

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deposits",
    )

    # ------------------------------------------------------
    # PAYMENT METHOD
    # ------------------------------------------------------

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD,
    )

    # ------------------------------------------------------
    # SENDER NAME
    # ------------------------------------------------------

    sender_name = models.CharField(
        max_length=100,
    )

    # ------------------------------------------------------
    # SENDER PHONE
    #
    # Form validation handles:
    # 09 + 6 to 9 digits
    # Total = 8 to 11 digits
    # ------------------------------------------------------

    sender_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )

    # ------------------------------------------------------
    # TRANSACTION ID
    # ------------------------------------------------------
    # Must be unique so the same payment cannot be
    # submitted multiple times.
    # ------------------------------------------------------

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
    )

    # ------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("1000.00")
            )
        ],
    )

    # ------------------------------------------------------
    # PAYMENT SCREENSHOT
    # ------------------------------------------------------

    screenshot = models.ImageField(
        upload_to="deposit_ss/",
    )

    # ------------------------------------------------------
    # USER NOTE
    # ------------------------------------------------------

    note = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # REQUEST STATUS
    # ------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending",
    )

    # ------------------------------------------------------
    # ADMIN REMARK
    # ------------------------------------------------------

    admin_remark = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # CREATED
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # ------------------------------------------------------
    # UPDATED
    # ------------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ------------------------------------------------------
    # APPROVAL INFORMATION
    # ------------------------------------------------------

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_deposit_requests",
    )

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(
                fields=["status"]
            ),

            models.Index(
                fields=["transaction_id"]
            ),

            models.Index(
                fields=["created_at"]
            ),

            models.Index(
                fields=["user", "status"]
            ),

        ]

    # ------------------------------------------------------
    # STRING
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"Deposit #{self.id} - "
            f"{self.user.username}"
        )


# ==========================================================
# WITHDRAW REQUEST
#
# User requests money from their wallet.
# Admin manually approves/rejects the request.
# ==========================================================

class WithdrawRequest(models.Model):

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    # ------------------------------------------------------
    # PAYMENT METHODS
    # ------------------------------------------------------

    PAYMENT_METHOD = (

        ("KBZ Pay", "KBZ Pay"),
        ("Wave Pay", "Wave Pay"),
        ("AYA Pay", "AYA Pay"),
        ("CB Pay", "CB Pay"),
        ("Bank Transfer", "Bank Transfer"),

    )

    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdraws",
    )

    # ------------------------------------------------------
    # PAYMENT METHOD
    # ------------------------------------------------------

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD,
    )

    # ------------------------------------------------------
    # RECEIVER NAME
    # ------------------------------------------------------

    receiver_name = models.CharField(
        max_length=100,
    )

    # ------------------------------------------------------
    # RECEIVER PHONE
    #
    # Form validation handles:
    # 09 + 6 to 9 digits
    # Total = 8 to 11 digits
    # ------------------------------------------------------

    receiver_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )

    # ------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("1000.00")
            )
        ],
    )

    # ------------------------------------------------------
    # USER NOTE
    # ------------------------------------------------------

    note = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # REQUEST STATUS
    # ------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending",
    )

    # ------------------------------------------------------
    # ADMIN REMARK
    # ------------------------------------------------------

    admin_remark = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # CREATED
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # ------------------------------------------------------
    # UPDATED
    # ------------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ------------------------------------------------------
    # APPROVAL INFORMATION
    # ------------------------------------------------------

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_withdraw_requests",
    )

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(
                fields=["status"]
            ),

            models.Index(
                fields=["created_at"]
            ),

            models.Index(
                fields=["user", "status"]
            ),

        ]

    # ------------------------------------------------------
    # STRING
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"Withdraw #{self.id} - "
            f"{self.user.username}"
        )


# ==========================================================
# WALLET TRANSACTION
#
# Permanent wallet history.
#
# Examples:
#
# Deposit
# Withdraw
# Payment
# Refund
#
# IMPORTANT:
# Do not delete transaction history after approval.
# ==========================================================

class WalletTransaction(models.Model):

    # ------------------------------------------------------
    # TRANSACTION TYPES
    # ------------------------------------------------------

    TRANSACTION_TYPES = (

        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
        ("Payment", "Payment"),
        ("Refund", "Refund"),

    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    # ------------------------------------------------------
    # WALLET
    # ------------------------------------------------------

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # ------------------------------------------------------
    # TRANSACTION TYPE
    # ------------------------------------------------------

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    # ------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01")
            )
        ],
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending",
    )

    # ------------------------------------------------------
    # DESCRIPTION
    # ------------------------------------------------------

    description = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # REFERENCE
    #
    # Examples:
    #
    # DepositRequest ID
    # WithdrawRequest ID
    # Order ID
    # Refund ID
    # ------------------------------------------------------

    reference_id = models.CharField(
        max_length=100,
        blank=True,
    )

    # ------------------------------------------------------
    # CREATED
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(
                fields=["wallet", "created_at"]
            ),

            models.Index(
                fields=["transaction_type"]
            ),

            models.Index(
                fields=["status"]
            ),

            models.Index(
                fields=["reference_id"]
            ),

        ]

    # ------------------------------------------------------
    # STRING
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"{self.transaction_type} - "
            f"{self.wallet.user.username} - "
            f"{self.amount}"
        )