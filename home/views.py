from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html")

def uploadFiles(request):
    return render(request, "multiple.html")