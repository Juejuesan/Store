from django.forms import Form
from django.shortcuts import render, redirect


def createPost(request):

    if request.method == "POST":

        form = Form(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = Form()

    return render( request,"createPost.html",{"form":form})