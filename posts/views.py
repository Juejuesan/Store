from django.shortcuts import render


def createPost(request):
    return render(request, 'createPost.html')