from django.db import models
from django.contrib.auth.models import User


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

    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"