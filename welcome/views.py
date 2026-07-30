from django.shortcuts import render

from posts.models import Post


def welcome_view(request):
    posts = Post.objects.filter(status="approved").order_by('-created_at')
    return render(request, 'welcome.html', {'posts': posts})



def about(request):
    return render(request, "about.html")