from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification


from django.contrib.auth.decorators import login_required

@login_required
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