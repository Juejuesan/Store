from notifications.models import Notification

def admin_notifications(request):

    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )

        print("Current User :", request.user.username)
        print("Notification Count :", notifications.count())

        return {
            "notification_count": notifications.count(),
            "admin_notifications": notifications
        }

    return {
        "notification_count": 0,
        "admin_notifications": []
    }