from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from posts.models import Post
from wishlist.models import Wishlist
from cart.models import StockHold


@login_required(login_url='welcome')
def home(request):
    search_query = request.GET.get('q', '').strip()

    posts = Post.objects.filter(
        status='approved'
    ).select_related(
        'category',
        'user',
        'user__user',
    ).prefetch_related(
        'items',
        'items__images',
        'items__size_variants',
    )

    # Search item name or category name
    if search_query:
        posts = posts.filter(
            Q(items__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()

    context = {
        'posts': posts,
        'search_query': search_query,
    }

    return render(request, 'home/home.html', context)


def viewdetail(request, post_id):
    # Get the main post
    post = get_object_or_404(
        Post,
        id=post_id,
        status="approved"
    )

    # Get similar posts
    similar_posts = Post.objects.filter(
        category=post.category,
        status="approved"
    ).exclude(
        id=post.id
    )[:3]

    # Get current user's wishlist posts
    wishlist_post_ids = []

    if request.user.is_authenticated:
        wishlist_post_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list(
            "post_id",
            flat=True
        )

    context = {
        "post": post,
        "similar_posts": similar_posts,
        "wishlist_post_ids": wishlist_post_ids,
    }

    return render(
        request,
        "home/viewdetail.html",
        context
    )


def createPost(request):
    return render(request, "posts/createPost.html")


def welcome(request):
    return render(request, "welcome/welcome.html")