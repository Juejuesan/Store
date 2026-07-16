from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def viewdetail(request):
    return render(request, "viewdetail.html")