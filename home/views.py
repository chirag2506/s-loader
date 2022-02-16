from django.shortcuts import render

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
        data = request.POST
        print(data)
        #     user = form.save()
        #     user.set_password(user.password)
        #     user.save()
        #     registered = True
        #     login(request, user)
        #     template = loader.get_template("login.html")
        #     return HttpResponse(template.render())
        # else:
        #     for msg in form.error_messages:
        #         print(form.error_messages[msg])
        #     return render(request=request,
        #                   template_name="signup.html",
        #                   context={"form": form})

def login_view(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user:
    #         if user.is_active:
    #             login(request,user)
    #             template = loader.get_template("index.html")
    #             return HttpResponse(template.render())
    #         else:
    #             return HttpResponse("Your account was inactive.")
    #     else:
    #         print("Someone tried to login and failed.")
    #         print("They used username: {} and password: {}".format(username,password))
    #         return HttpResponse("Invalid login details given")
    # else:
    #     return HttpResponseRedirect() #add error page link
    # if request.method == 'POST':  
    data = request.POST
    print(data)
    return render(request, "home.html")