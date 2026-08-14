from django.urls import path
from . import views


urlpatterns = [
    path('createPost/', views.create_post, name='createPost'),
    path('get-category-sizes/<int:category_id>/', views.get_category_sizes, name='get_category_sizes'),
]