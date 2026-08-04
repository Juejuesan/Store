from django.db import transaction
from django.utils import timezone
from django.db.models import F

from wallet.models import (
    Wallet,
    WalletTransaction,
)


# ==========================================================
# APPROVE DEPOSIT
# ==========================================================

@transaction.atomic
def approve_deposit(deposit, approved_by=None):
    """
    Approve a pending deposit request.

    - Add money to wallet
    - Update deposit status
    - Create wallet transaction
    """

    if deposit.status != "Pending":
        raise ValueError("Deposit already processed.")

    wallet = Wallet.objects.select_for_update().get(
        pk=deposit.wallet.pk
    )



    wallet.balance = F("balance") + deposit.amount
    wallet.save(update_fields=["balance"])
    wallet.refresh_from_db()

    wallet.save(
        update_fields=["balance"]
    )

    deposit.status = "Approved"

    # If these fields exist in your model
    if hasattr(deposit, "approved_by"):
        deposit.approved_by = approved_by

    if hasattr(deposit, "approved_at"):
        deposit.approved_at = timezone.now()

    deposit.save()

    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Deposit",
        amount=deposit.amount,
        status="Approved",
        description=f"Deposit via {deposit.payment_method}",
    )

    return True


# ==========================================================
# REJECT DEPOSIT
# ==========================================================

@transaction.atomic
def reject_deposit(deposit, approved_by=None):
    """
    Reject a pending deposit request.
    """

    if deposit.status != "Pending":
        return False

    deposit.status = "Rejected"

    if hasattr(deposit, "approved_by"):
        deposit.approved_by = approved_by

    if hasattr(deposit, "approved_at"):
        deposit.approved_at = timezone.now()

    deposit.save()

    return True


# ==========================================================
# APPROVE WITHDRAW
# ==========================================================

@transaction.atomic
def approve_withdraw(withdraw, approved_by=None):
    """
    Approve withdrawal request.

    - Deduct wallet balance
    - Update request
    - Save transaction
    """

    if withdraw.status != "Pending":
        raise ValueError("Withdraw already processed.")

    wallet = Wallet.objects.select_for_update().get(
        pk=withdraw.wallet.pk
    )

    if wallet.balance < withdraw.amount:
        raise ValueError(
            "Insufficient wallet balance."
        )

    wallet.balance -= withdraw.amount

    wallet.save(
        update_fields=["balance"]
    )

    withdraw.status = "Approved"

    if hasattr(withdraw, "approved_by"):
        withdraw.approved_by = approved_by

    if hasattr(withdraw, "approved_at"):
        withdraw.approved_at = timezone.now()

    withdraw.save()

    WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="Withdraw",
        amount=withdraw.amount,
        status="Approved",
        description=f"Withdraw via {withdraw.payment_method}",
    )

    return True


# ==========================================================
# REJECT WITHDRAW
# ==========================================================

@transaction.atomic
def reject_withdraw(withdraw, approved_by=None):
    """
    Reject withdrawal request.
    """

    if withdraw.status != "Pending":
        return False

    withdraw.status = "Rejected"

    if hasattr(withdraw, "approved_by"):
        withdraw.approved_by = approved_by

    if hasattr(withdraw, "approved_at"):
        withdraw.approved_at = timezone.now()

    withdraw.save()

    return True