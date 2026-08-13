from django.conf import settings
from django.db import models

from home.models import Post


class Wishlist(models.Model):
    """
    Stores products that a user has added to their wishlist.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_wishlist",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.post}"