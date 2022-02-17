from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from sloader.constants import msg_d

# Create your views here.

def login(request):
    return render(request, "login.html")

# def home(request):
#     return render(request, "home.html")

def uploadFiles(request):
    return render(request, "multiple.html")

def signup(request):
    registered = False
    if request.method == 'POST':  
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        conf_password = request.POST.get('ConfPassword')
        if(password == conf_password):
            user = User(name= username, email = email, password = password)
            user.save()
            print("success register")
            messages.success(request, msg_d['signup_success'])
            return redirect('/home')
        else:
            print("not register")
            messages.error(request, msg_d['not_match_password'])
            return render(request, "login.html")

def home(request):
    return render(request,'home.html')


def login_view(request):
    if request.method=='POST':  
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username, password)
        if not username:
            raise ValueError('Please enter user name')
        data = User.objects.raw('select * from home_user where email = %s and password = %s', [username, password])
        if(data):
            print(data)
            print("Login successfull")
            messages.success(request, msg_d["login_success"])
            return redirect('/home')
        else:
            print("Enter valide data")
            messages.error(request, msg_d['invalid_data'])
            return redirect("/")
