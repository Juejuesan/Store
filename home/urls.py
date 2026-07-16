from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("viewdetail/", views.viewdetail, name="viewdetail"),
]