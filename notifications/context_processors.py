from .models import Notification


def user_notifications(request):

    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )

        return {
            "notification_count": notifications.count(),
            "user_notifications": notifications
        }


    return {
        "notification_count": 0,
        "user_notifications": []
    }