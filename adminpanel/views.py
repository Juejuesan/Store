from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from posts.models import Post
from notifications.models import Notification


# ==========================
# Dashboard
# ==========================
def dashboard(request):
    context = {
        "total_users": User.objects.filter(is_active=True).count(),
        "total_sellers": User.objects.count(),
        "pending_posts": Post.objects.filter(
            status="pending"
        ).count(),
        "pending_orders": 15,
        "total_revenue": "15,800,000",
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post


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

    context = {
        "post": post,
    }

    return render(
        request,
        "adminpanel/post_detail.html",
        context,
    )


def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = 'approved'
    post.save()
    messages.success(request, f'Post #{post.id} has been approved.')
    return redirect('posts')


def reject_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = 'rejected'
    post.save()
    messages.success(request, f'Post #{post.id} has been rejected.')
    return redirect('posts')

from django.contrib.auth.decorators import login_required

@login_required
def read_notification(request, noti_id):

    notification = get_object_or_404(
        Notification,
        id=noti_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    if notification.notification_type == "new_post":
        return redirect("posts")

    return redirect("dashboard")