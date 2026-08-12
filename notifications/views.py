from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Notification


# =========================================================
# NOTIFICATION PAGE
# =========================================================

@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications/notifications.html",
        {
            "notifications": notification_list
        }
    )


# =========================================================
# AJAX BELL COUNT
# =========================================================

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


# =========================================================
# AJAX DROPDOWN
# =========================================================

@login_required
def notification_dropdown(request):

    notification_list = Notification.objects.filter(
        user=request.user
    ).exclude(
        notification_type__in=[
            "deposit_request",
            "new_post",
        ]
    ).order_by("-created_at")[:10]

    data = []

    for notification in notification_list:

        data.append({
            "id": notification.id,

            "message": notification.message,

            "time": notification.created_at.strftime(
                "%b %d %I:%M %p"
            ),

            "is_read": notification.is_read,

            "target_url": notification.target_url,
        })

    return JsonResponse({
        "notifications": data
    })


# =========================================================
# AJAX MARK ONE NOTIFICATION AS READ
# =========================================================

@login_required
@require_POST
def ajax_read_notification(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    notification.is_read = True

    notification.save(
        update_fields=["is_read"]
    )

    return JsonResponse({
        "success": True,
        "id": notification.id
    })


# =========================================================
# AJAX MARK ALL NOTIFICATIONS AS READ
# =========================================================

@login_required
@require_POST
def ajax_mark_all_read(request):

    updated = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).exclude(
        notification_type__in=[
            "deposit_request",
            "new_post",
        ]
    ).update(
        is_read=True
    )

    return JsonResponse({
        "success": True,
        "updated": updated
    })


# =========================================================
# AJAX DELETE ONE NOTIFICATION
# =========================================================

@login_required
@require_POST
def ajax_delete_notification(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    notification.delete()

    return JsonResponse({
        "success": True,
        "deleted_id": id
    })


# =========================================================
# AJAX DELETE SELECTED NOTIFICATIONS
# =========================================================

@login_required
@require_POST
def ajax_delete_selected(request):

    notification_ids = request.POST.getlist(
        "notification_ids[]"
    )

    if not notification_ids:

        return JsonResponse({
            "success": False,
            "message": "No notifications selected."
        }, status=400)

    deleted_count = Notification.objects.filter(
        user=request.user,
        id__in=notification_ids
    ).delete()[0]

    return JsonResponse({
        "success": True,
        "deleted_count": deleted_count
    })


# =========================================================
# AJAX DELETE ALL NOTIFICATIONS
# =========================================================

@login_required
@require_POST
def ajax_delete_all(request):

    deleted_count = Notification.objects.filter(
        user=request.user
    ).delete()[0]

    return JsonResponse({
        "success": True,
        "deleted_count": deleted_count
    })