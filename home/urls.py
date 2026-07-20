from django.urls import path
from . import views

urlpatterns = [
    # If your coworker already made a home view function inside home/views.py,
    # you can link it here. For now, this empty path satisfies Django.
    # path('', views.home_view, name='home'),
    path('', views.home, name='home'),
    path("viewdetail/", views.viewdetail, name="viewdetail"),
path("createPost/", views.createPost, name="createPost")
]