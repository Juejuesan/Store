from django.urls import path

from home import views
from posts.urls import urlpatterns

urlpatterns=[
    path('',views.home,name='home'),
]