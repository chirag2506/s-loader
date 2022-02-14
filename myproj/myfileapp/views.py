from django.shortcuts import render,HttpResponse
from .models import myuploadfile

# Create your views here.
def index(request):
    return render(request,"index.html")

def send_files(request):
    if request.method == "POST":
        name =request.POST.get("filename")
        myfile = request.FILES.getlist("uploadfiles")
        for f in myfile:
            myuploadfile(f_name=name,myfiles=f).save()
       # print(myfile)
        return HttpResponse("File Uploaded Successfully")