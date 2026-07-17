from django.urls import path

from posts import views

urlpatterns = [
    path('createPost/',views.createPost,name='createPost'),
]