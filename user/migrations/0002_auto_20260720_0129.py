from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.db.models import Model


def create_test_users(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("user", "Profile")   # Change "user" if your app name is different

    # Approved user
    approved_user, created = User.objects.get_or_create(
        username="testApprove",
        defaults={
            "email": "test01@gmail.com",
            "password": make_password("Test@000"),
        }
    )

    approved_profile = Profile(
        user=approved_user,
        phone_number="09111111111",
        address="Yangon",
        gender="M",
        status="Approved",
    )
    approved_profile.save()

    # Banned user
    banned_user, created = User.objects.get_or_create(
        username="testBan",
        defaults={
            "email": "test02@gmail.com",
            "password": make_password("Test@000"),
        }
    )

    banned_profile = Profile(
        user=banned_user,
        phone_number="09222222222",
        address="Yangon",
        gender="M",
        status="Banned",
    )
    banned_profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),  # Change if needed
    ]

    operations = [
        migrations.RunPython(create_test_users),
    ]