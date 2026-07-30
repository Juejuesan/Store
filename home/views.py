from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

def viewdetail(request):
    return render(request, "home/viewdetail.html")

def createPost(request):
    return render(request, "posts/createPost.html")