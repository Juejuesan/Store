from django.http import JsonResponse

from .models import Notification


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