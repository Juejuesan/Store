from notifications.models import Notification


def admin_notifications(request):

    if request.user.is_authenticated:

        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()


        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by("-created_at")


        return {

            "notification_count": count,

            "admin_notifications": notifications

        }


    return {

        "notification_count":0,

        "admin_notifications":[]

    }