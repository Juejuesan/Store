import random

from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(profile):
    code = str(random.randint(100000, 999999))

    profile.verification_code = code
    profile.save()

    send_mail(
        subject="Verify Your TurstyShop Account",
        message=f"""
Hello {profile.user.username},

Your verification code is:

{code}

Thank you for joining TurstyShop!
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[profile.user.email],
        fail_silently=False,
    )