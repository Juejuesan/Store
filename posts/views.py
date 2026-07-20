from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.form import PostForm
from posts.models import PostImage
from notifications.models import Notification
from django.contrib.auth.models import User

@login_required
def createPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user

            post.save()

            # notify admin

            # notify admin

            admins = User.objects.filter(
                is_staff=True
            )

            for admin in admins:
                Notification.objects.create(

                    user=admin,

                    post=post,

                    message="New post waiting for approval",

                    notification_type="pending"

                )
            # ==============================
            # SEND NOTIFICATION TO ADMIN
            # ==============================

            admins = User.objects.filter(
                is_staff=True
            )

            for admin in admins:
                Notification.objects.create(

                    user=admin,

                    post=post,

                    message=f"{request.user.username} created a new post waiting approval",

                    notification_type="post_request"

                )
                # end

            images = request.FILES.getlist('images')

            for img in images:
                PostImage.objects.create(
                    post=post,
                    image=img
                )
            return redirect("home")

    else:
        form = PostForm()

    return render(request, "posts/createPost.html", {"form": form})