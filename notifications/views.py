from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Notification


# ===========================================
# Notification Page
# ===========================================

@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")


    return render(
        request,
        "notifications/notifications.html",
        {
            "notifications": notifications
        }
    )



# ===========================================
# AJAX Bell Count
# ===========================================

@login_required
def notification_count(request):

    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).exclude(
        notification_type__in=[
            "deposit_request",
            "new_post",
        ]
    ).count()


    return JsonResponse({

        "count": count

    })



# ===========================================
# AJAX Dropdown
# ===========================================

@login_required
def notification_dropdown(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).exclude(
        notification_type__in=[
            "deposit_request",
            "new_post",
        ]
    ).order_by(
        "-created_at"
    )[:10]


    data = []


    for n in notifications:

        data.append({

            "id": n.id,

            "message": n.message,

            "time": n.created_at.strftime(
                "%b %d %I:%M %p"
            ),

            "is_read": n.is_read,

        })


    return JsonResponse({

        "notifications": data

    })



# ===========================================
# AJAX Mark Read
# ===========================================

@login_required
def ajax_read_notification(request, id):

    notification = get_object_or_404(

        Notification,

        id=id,

        user=request.user

    )


    notification.is_read = True

    notification.save()


    return JsonResponse({

        "success": True

    })