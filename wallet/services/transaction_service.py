from wallet.models import WalletTransaction


def create_transaction(
    wallet,
    transaction_type,
    amount,
    description=""
):
    """
    Create wallet transaction history.
    """

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type=transaction_type,
        amount=amount,
        balance_after=wallet.balance,
        description=description,
    )