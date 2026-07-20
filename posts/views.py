from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.form import PostForm
from posts.models import PostImage
from user.models import Profile


@login_required()
def createPost(request):
    user = Profile.objects.get(user=request.user)

    if user.STATUS == 'banned' :
        messages.error(request, "Your account is not approved yet.")
        return redirect('home')
    else:

        if request.method == "POST":
         form = PostForm(request.POST, request.FILES)

         if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user

            post.save()

            images = request.FILES.getlist('images')

            if len(images) == 0:
                messages.error(request, "Please upload at least one photo.")
                return render(request, "posts/createPost.html", {"form": form})

            if len(images) > 5:
                messages.error(request, "You can upload a maximum of 5 photos.")

            for img in images:
                PostImage.objects.create(
                    post=post,
                    image=img
                )
            return redirect("home")

        else:
            form = PostForm()

        return render(request, "posts/createPost.html", {"form": form})