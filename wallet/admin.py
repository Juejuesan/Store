from django.contrib import admin
from django.utils import timezone

from .models import (
    Wallet,
    DepositRequest,
    WithdrawRequest,
    WalletTransaction,
)

from notifications.models import Notification



@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "amount",
        "status",
        "created_at",
    )


    actions = [
        "approve_deposit"
    ]


    def approve_deposit(self, request, queryset):

        for deposit in queryset:

            if deposit.status == "Pending":


                # Change status

                deposit.status = "Approved"

                deposit.approved_at = timezone.now()

                deposit.approved_by = request.user

                deposit.save()



                # Add money to wallet

                wallet, created = Wallet.objects.get_or_create(
                    user=deposit.user
                )


                wallet.balance += deposit.amount

                wallet.save()



                # Create transaction

                from .models import WalletTransaction

                WalletTransaction.objects.create(

                    wallet=wallet,

                    transaction_type="Deposit",

                    amount=deposit.amount,

                    status="Approved",

                    description="Deposit approved by admin",

                    reference_id=str(deposit.id)

                )



                # Notify User

                Notification.objects.create(

                    user=deposit.user,

                    message=(
                        f"Your wallet has been updated. "
                        f"{deposit.amount} MMK added successfully."
                    ),

                    notification_type="deposit_approved"

                )



        self.message_user(
            request,
            "Selected deposits approved successfully."
        )


    approve_deposit.short_description = (
        "Approve selected deposits"
    )




admin.site.register(Wallet)
admin.site.register(DepositRequest)
admin.site.register(WithdrawRequest)
admin.site.register(WalletTransaction)