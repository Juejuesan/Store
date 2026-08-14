from django.urls import path

from .views import image_search_view


app_name = "image_search"


urlpatterns = [
    path(
        "",
        image_search_view,
        name="search"
    ),
]