# adminpanel/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name="dashboard"),

    path('posts/', views.posts, name="posts"),



]