from notifications.models import Notification


def admin_notifications(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return {
            "admin_notifications": [],
            "notification_count": 0,
        }

    notifications = Notification.objects.filter(

        notification_type__in=[
            "new_post",
            "deposit_request",
            "withdraw_request",
        ],

        is_read=False

    ).order_by("-created_at")

    return {

        "admin_notifications": notifications,

        "notification_count": notifications.count(),

    }