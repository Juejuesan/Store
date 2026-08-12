from django.db import models
from django.contrib.auth.models import User


class AdminActivity(models.Model):

    ACTION_CHOICES = [
        ("ban_user", "You banned a user"),
        ("unban_user", "You unbanned a user"),

        ("approve_deposit", "You approved a deposit"),
        ("reject_deposit", "You rejected a deposit"),

        ("approve_withdraw", "You approved a withdrawal"),
        ("reject_withdraw", "You rejected a withdrawal"),

        ("approve_post", "You approved a post"),
        ("reject_post", "You rejected a post"),
    ]

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admin_activities"
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    message = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message or self.get_action_display()