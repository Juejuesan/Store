from django.urls import path
from . import views

urlpatterns = [

    # Notification Page
    path(
        "",
        views.notifications,
        name="notifications",
    ),

    # Bell Count AJAX
    path(
        "count/",
        views.notification_count,
        name="notification_count",
    ),

]