from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # CREATE POST
    # =====================================================

    path(
        "createPost/",
        views.create_post,
        name="createPost",
    ),

    # =====================================================
    # MY POSTS
    # =====================================================

    path(
        "my-posts/",
        views.my_posts,
        name="my_posts",
    ),

    # =====================================================
    # CATEGORY SIZES
    # =====================================================

    path(
        "get-category-sizes/<int:category_id>/",
        views.get_category_sizes,
        name="get_category_sizes",
    ),
]