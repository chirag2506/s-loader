from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from sloader.constants import msg_d
from grouping.views import select
from django.contrib.auth.decorators import login_required
from charts.models import StoreData

# Create your views here.
# @login_required
def login(request):
    return render(request, "login.html")

# def home(request):
#     return render(request, "home.html")
# @login_required(login_url="")
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
            # s=StoreData(naam=username)
            # s.save()
            print("success register")
            messages.success(request, msg_d['signup_success'])
            return redirect('/home')
        else:
            print("not register")
            messages.error(request, msg_d['not_match_password'])
            return render(request, "login.html")

# @login_required
def home(request):
    return render(request,'home.html')


def login_view(request):
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        # print(username, password)
        if not username:
            raise ValueError('Please enter user name')
        data = User.objects.raw('select * from home_user where email = %s and password = %s', [username, password])

        if(data):
            # a=User.objects.get(email=username)
            # s=StoreData(naam=a)
            # s.save()
            # print("ye raha usename:",try1,username)
            messages.success(request, msg_d["login_success"])
            return redirect("/home")
        else:
            # print("Enter valid data")
            messages.error(request, msg_d['invalid_data'])
            return redirect("/")
