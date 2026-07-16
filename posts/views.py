from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.form import PostForm
from posts.models import PostImage
from user.models import User

@login_required
def createPost(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user

            post.save()

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