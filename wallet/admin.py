from django.contrib import admin
from .models import Wallet, DepositRequest, WithdrawRequest

admin.site.register(Wallet)
admin.site.register(DepositRequest)
admin.site.register(WithdrawRequest)