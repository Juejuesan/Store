from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name="dashboard"),

    path('posts/', views.posts, name="posts"),

    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name="post_detail"
    ),

    path(
        'posts/<int:post_id>/approve/',
        views.approve_post,
        name="approve_post"
    ),

    path(
        'posts/<int:post_id>/reject/',
        views.reject_post,
        name="reject_post"
    ),

]