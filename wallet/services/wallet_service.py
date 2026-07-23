from decimal import Decimal

from django.db import transaction

from wallet.models import Wallet

from .transaction_service import create_transaction


@transaction.atomic
def increase_balance(
    wallet: Wallet,
    amount,
    transaction_type="Deposit",
    description=""
):

    amount = Decimal(amount)

    wallet.balance += amount

    wallet.save()

    create_transaction(
        wallet,
        transaction_type,
        amount,
        description
    )

    return wallet


@transaction.atomic
def decrease_balance(
    wallet: Wallet,
    amount,
    transaction_type="Withdraw",
    description=""
):

    amount = Decimal(amount)

    if wallet.balance < amount:
        raise ValueError("Insufficient balance.")

    wallet.balance -= amount

    wallet.save()

    create_transaction(
        wallet,
        transaction_type,
        -amount,
        description
    )

    return wallet