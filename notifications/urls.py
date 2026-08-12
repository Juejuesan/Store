from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.notifications,
        name="notifications"
    ),

    path(
        "count/",
        views.notification_count,
        name="notification_count"
    ),

    path(
        "dropdown/",
        views.notification_dropdown,
        name="notification_dropdown"
    ),

    path(
        "read/<int:id>/",
        views.ajax_read_notification,
        name="ajax_read_notification"
    ),

    path(
        "mark-all-read/",
        views.ajax_mark_all_read,
        name="ajax_mark_all_read"
    ),

    path(
        "delete/<int:id>/",
        views.ajax_delete_notification,
        name="ajax_delete_notification"
    ),

    path(
        "delete-selected/",
        views.ajax_delete_selected,
        name="ajax_delete_selected"
    ),

    path(
        "delete-all/",
        views.ajax_delete_all,
        name="ajax_delete_all"
    ),
]