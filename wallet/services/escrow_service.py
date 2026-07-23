from decimal import Decimal

from django.db import transaction

from .transaction_service import create_transaction


@transaction.atomic
def hold_money(wallet, amount):

    amount = Decimal(amount)

    if wallet.balance < amount:
        raise ValueError("Insufficient balance.")

    wallet.balance -= amount

    wallet.frozen_balance += amount

    wallet.save()

    create_transaction(

        wallet,

        "Escrow Hold",

        -amount,

        "Money held in escrow"

    )

    return wallet


@transaction.atomic
def release_money(
    buyer_wallet,
    seller_wallet,
    amount
):

    amount = Decimal(amount)

    if buyer_wallet.frozen_balance < amount:
        raise ValueError("Frozen balance error.")

    buyer_wallet.frozen_balance -= amount

    buyer_wallet.save()

    seller_wallet.balance += amount

    seller_wallet.save()

    create_transaction(

        buyer_wallet,

        "Escrow Release",

        -amount,

        "Escrow released"

    )

    create_transaction(

        seller_wallet,

        "Deposit",

        amount,

        "Escrow payment received"

    )


@transaction.atomic
def refund_money(wallet, amount):

    amount = Decimal(amount)

    if wallet.frozen_balance < amount:
        raise ValueError("Frozen balance error.")

    wallet.frozen_balance -= amount

    wallet.balance += amount

    wallet.save()

    create_transaction(

        wallet,

        "Refund",

        amount,

        "Escrow refunded"

    )