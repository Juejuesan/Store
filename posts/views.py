import profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from notifications.models import Notification
from posts.form import PostForm
from posts.models import PostImage, Post
from user.models import Profile


@login_required
def createPost(request):
    user = Profile.objects.get(user=request.user)

    if user.status == "Banned":
        messages.error(request, "Your account has been banned.")
        return render(request, "home/home.html", {
        "profile": profile,

    })

    else:
        request.method == "POST"
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()

            # Notifications

            # Create notification for every admin

            admins = User.objects.filter(is_staff=True)

            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    post=post,
                    message=f"{request.user.username} created a new {post.category.name} post waiting for approval.",
                    notification_type="new_post"
                )
            images = request.FILES.getlist("images")

            if len(images) == 0:
                post.delete()
                messages.error(request, "Please upload at least one photo.")
                return render(request, "posts/createPost.html", {"form": form})

            if len(images) > 5:
                post.delete()
                messages.error(request, "You can upload a maximum of 5 photos.")
                return render(request, "posts/createPost.html", {"form": form})

            for img in images:
                PostImage.objects.create(
                    post=post,
                    image=img
                )

            messages.success(request, "Your Post is pending to approve by admin.")
            return redirect("home")

        else:
         form = PostForm()

    return render(request, "posts/createPost.html", {"form": form})

def showPost(request):
    posts = Post.objects.filter(status="approved")
    return render(request, "posts/showPost.html", {"posts": posts})