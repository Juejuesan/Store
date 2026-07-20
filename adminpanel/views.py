from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from posts.models import Post
from notifications.models import Notification


# ==========================
# Dashboard
# ==========================
def dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_sellers": User.objects.count(),
        "pending_posts": Post.objects.filter(
            status="pending"
        ).count(),
        "pending_orders": 15,
        "revenue": "15,800,000 MMK",
        "recent_activities": [
            {
                "activity": "New Seller Registered",
                "user": "Ko Ko",
                "status": "Success",
                "time": "2 mins ago",
            },
            {
                "activity": "Product Submitted",
                "user": "Su Su",
                "status": "Pending",
                "time": "10 mins ago",
            },
            {
                "activity": "Wallet Top Up",
                "user": "Mg Mg",
                "status": "Completed",
                "time": "35 mins ago",
            },
            {
                "activity": "Account Warning",
                "user": "Aung Aung",
                "status": "Warning",
                "time": "1 hour ago",
            },
        ],
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
    )


# ==========================
# Pending Posts
# ==========================
def posts(request):
    pending_posts = Post.objects.filter(
        status="pending"
    ).order_by("-created_at")

    context = {
        "pending_posts": pending_posts,
    }

    return render(
        request,
        "adminpanel/posts.html",
        context,
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(
        request,
        "adminpanel/post_detail.html",
        {
            "post": post,
        },
    )


def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.status = "approved"
    post.save()

    Notification.objects.create(
        user=post.user,
        post=post,
        message="Your post has been approved.",
        notification_type="approved",
    )

    return redirect("posts")


def reject_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.status = "rejected"
    post.save()

    Notification.objects.create(
        user=post.user,
        post=post,
        message="Your post has been rejected.",
        notification_type="rejected",
    )

    return redirect("posts")