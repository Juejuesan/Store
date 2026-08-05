from .models import Notification

def notification_context(request):

    if request.user.is_authenticated:

        user_notification_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).exclude(
            notification_type__in=[
                "deposit_request",
                "new_post",
            ]
        ).count()

        admin_notification_count = 0

        if request.user.is_staff:

            admin_notification_count = Notification.objects.filter(
                is_read=False,
                notification_type__in=[
                    "deposit_request",
                    "new_post",
                ]
            ).count()

    else:

        user_notification_count = 0
        admin_notification_count = 0

    return {

        "user_notification_count": user_notification_count,

        "admin_notification_count": admin_notification_count,

    }