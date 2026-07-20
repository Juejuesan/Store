from django.shortcuts import render
from .models import Notification



def notifications(request):

    data = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )


    return render(
        request,
        "notifications/notification.html",
        {
            "notifications":data
        }
    )