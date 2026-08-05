from django.contrib import admin

from .models import (
    Wallet,
    DepositRequest,
    WithdrawRequest,
    WalletTransaction,
)


admin.site.register(Wallet)
admin.site.register(DepositRequest)
admin.site.register(WithdrawRequest)
admin.site.register(WalletTransaction)