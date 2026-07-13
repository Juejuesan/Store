from django.urls import path

from posts import views
from trustyshop import urls

urlpatterns = [
    path('createPost/',views.createPost,name='createPost'),
]