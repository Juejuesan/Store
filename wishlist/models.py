from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_wishlist_post",
            ),
        ]

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.post}"
        )