from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        views.home,
        name='home'
    ),


    # =====================================================
    # PRODUCT DETAIL
    # =====================================================

    path(
        'viewdetail/<int:post_id>/',
        views.viewdetail,
        name='viewdetail'
    ),

]