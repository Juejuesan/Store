from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('top-up/', views.top_up, name='top_up'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('sell/', views.sell_item, name='sell'),
    path('buy/<int:post_id>/', views.buy_item, name='buy_item'),
]