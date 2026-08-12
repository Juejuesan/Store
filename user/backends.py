from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        **kwargs
    ):

        if not username or not password:
            return None

        try:

            user = User.objects.get(
                Q(username__iexact=username)
                | Q(email__iexact=username)
            )

        except User.DoesNotExist:

            return None

        # User inactive ဖြစ်ရင် login မဝင်စေ
        if not self.user_can_authenticate(user):
            return None

        # Password hash ကို Django နဲ့စစ်
        if user.check_password(password):
            return user

        return None

    def user_can_authenticate(self, user):

        return user.is_active