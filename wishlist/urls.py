from django.urls import path

from . import views


app_name = "wishlist"


urlpatterns = [

    path(
        "",
        views.wishlist,
        name="wishlist",
    ),

    path(
        "add/<int:post_id>/",
        views.add_to_wishlist,
        name="add",
    ),

    path(
        "remove/<int:post_id>/",
        views.remove_from_wishlist,
        name="remove",
    ),

]