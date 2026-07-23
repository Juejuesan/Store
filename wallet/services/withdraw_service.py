from django.db import transaction
from django.utils import timezone

from .wallet_service import decrease_balance


@transaction.atomic
def approve_withdraw(withdraw):

    if withdraw.status != "Pending":
        raise ValueError("Withdraw already processed.")

    decrease_balance(

        wallet=withdraw.user.wallet,

        amount=withdraw.amount,

        transaction_type="Withdraw",

        description=f"Withdraw via {withdraw.payment_method}"

    )

    withdraw.status = "Approved"

    withdraw.approved_at = timezone.now()

    withdraw.save()

    return withdraw


@transaction.atomic
def reject_withdraw(withdraw, remark=""):

    if withdraw.status != "Pending":
        raise ValueError("Withdraw already processed.")

    withdraw.status = "Rejected"

    withdraw.admin_remark = remark

    withdraw.approved_at = timezone.now()

    withdraw.save()

    return withdraw