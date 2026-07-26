from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Check if the user exists by matching username OR email (case-insensitive)
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # In case multiple users share an email (if email isn't set to unique)
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).order_by('id').first()

        # Check the password and if the user is allowed to authenticate (e.g., is_active)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None