from django.urls import path
from . import views


urlpatterns = [
    path('',views.welcome_view,name='welcome'),
    path('about/', views.about,name='about'),
]