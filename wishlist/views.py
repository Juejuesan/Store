from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post

from .models import Wishlist


# ==========================================================
# WISHLIST PAGE
# ==========================================================
@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        "post",
        "post__user",
        "post__category",
    ).prefetch_related(
        "post__items",
        "post__items__images",
        "post__items__size_variants",
    )

    return render(
        request,
        "wishlist/wishlist.html",
        {
            "wishlist_items": wishlist_items,
        },
    )
# ==========================================================
# ADD TO WISHLIST
# ==========================================================

@login_required
def add_to_wishlist(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status="approved",
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        post=post,
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "wishlist:wishlist",
        )
    )


# ==========================================================
# REMOVE FROM WISHLIST
# ==========================================================

@login_required
def remove_from_wishlist(request, post_id):

    Wishlist.objects.filter(
        user=request.user,
        post_id=post_id,
    ).delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "wishlist:wishlist",
        )
    )