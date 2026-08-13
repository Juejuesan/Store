from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from cart.models import StockHold
from posts.models import Post


@login_required(login_url='welcome')
def home(request):
    posts = Post.objects.filter(status="approved").order_by('-created_at')
    return render(request, "home/home.html", {"posts": posts})


def viewdetail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="approved")

    similar_posts = Post.objects.filter(
        category=post.category,
        status="approved"
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'similar_posts': similar_posts
    }
    return render(request, 'home/viewdetail.html', context)


def createPost(request):
    return render(request, "posts/createPost.html")


def welcome(request):
    return render(request, "welcome/welcome.html")