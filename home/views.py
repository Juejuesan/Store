from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def viewdetail(request):
    return render(request, "viewdetail.html")

def createPost(request):
    return render(request, "createPost.html")