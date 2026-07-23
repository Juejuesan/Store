from django.db import transaction
from django.utils import timezone

from .wallet_service import increase_balance


@transaction.atomic
def approve_deposit(deposit):

    if deposit.status != "Pending":
        raise ValueError("Deposit already processed.")

    increase_balance(

        wallet=deposit.user.wallet,

        amount=deposit.amount,

        transaction_type="Deposit",

        description=f"Deposit via {deposit.payment_method}"

    )

    deposit.status = "Approved"

    deposit.approved_at = timezone.now()

    deposit.save()

    return deposit


@transaction.atomic
def reject_deposit(deposit, remark=""):

    if deposit.status != "Pending":
        raise ValueError("Deposit already processed.")

    deposit.status = "Rejected"

    deposit.admin_remark = remark

    deposit.approved_at = timezone.now()

    deposit.save()

    return deposit