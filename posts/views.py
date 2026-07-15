from django.shortcuts import render, redirect
from posts.form import PostForm


def createPost(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = PostForm()

    return render(request, "createPost.html", {"form": form})