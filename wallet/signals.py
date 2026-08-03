from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Wallet


# ==========================================================
# CREATE WALLET AUTOMATICALLY
# ==========================================================

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    """
    Automatically create a wallet whenever
    a new user registers.
    """

    if created:

        Wallet.objects.create(
            user=instance
        )


# ==========================================================
# SAVE WALLET
# ==========================================================

@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    """
    Save wallet whenever user is saved.
    """

    if hasattr(instance, "wallet"):

        instance.wallet.save()