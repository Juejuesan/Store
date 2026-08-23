from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # CREATE POST
    # =====================================================

    path(
        "createPost/",
        views.create_post,
        name="createPost"
    ),


    # =====================================================
    # MY POSTS
    # =====================================================

    path(
        "my-posts/",
        views.my_posts,
        name="my_posts"
    ),


    # =====================================================
    # GET CATEGORY SIZES
    # =====================================================

    path(
        "get-category-sizes/<int:category_id>/",
        views.get_category_sizes,
        name="get_category_sizes"
    ),


    # =====================================================
    # EDIT POST
    # =====================================================

    path(
        "editPost/<int:post_id>/",
        views.edit_post,
        name="editPost"
    ),





    # =====================================================
    # PENDING POST DETAIL
    # =====================================================

    path(
        'pending/<int:post_id>/',
        views.pending_post_detail,
        name='pending_post_detail'
    ),




    # =====================================================
    # SOLD POST DETAIL
    # =====================================================

    path(
        'sold/<int:post_id>/',
        views.sold_post_detail,
        name='sold_post_detail'
    ),


  


    # =====================================================
    # REJECTED POST DETAIL
    # =====================================================

    path(
        'rejected/<int:post_id>/',
        views.rejected_post_detail,
        name='rejected_post_detail'
    ),

]