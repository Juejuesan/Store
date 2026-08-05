from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("new_post", "New Post"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("deposit_request", "Deposit Request"),
        ("deposit_approved", "Deposit Approved"),
        ("deposit_rejected", "Deposit Rejected"),
    ]

    target_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    message = models.CharField(
        max_length=255
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    target_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message