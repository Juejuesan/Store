from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404

from posts.models import Post
from wishlist.models import Wishlist

@login_required(login_url='welcome')
def home(request):
    posts = Post.objects.filter(status="approved").order_by('-created_at')

    return render(request, "home/home.html", {"posts": posts})

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