from django.db import models


from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    STATUS = [
        ("Approved", "Approved"),
        ("Banned", "Banned"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )

    fullName = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    address = models.CharField(
        max_length=200
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Approved"
    )

    email_verified = models.BooleanField(
        default=False
    )

    terms_accepted = models.BooleanField(
        default=False
    )

    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # =========================================================


# PASSWORD RESET OTP
# =========================================================

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_otps"
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"Password OTP for {self.user.username}"