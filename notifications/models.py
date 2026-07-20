from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('pending','Pending'),
    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True
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


    def __str__(self):
        return self.message