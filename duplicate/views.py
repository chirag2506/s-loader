from csv import excel
from urllib import request
from django.shortcuts import render, HttpResponse
from .models import FilesUpload
import pandas as pd
import pip
# pip.main(["install", "openpyxl"])
import json

# Create your views here.
def home(request):
    if request.method == "POST":
        excel_file = request.FILES["myFile"]
        wb = pd.read_excel(excel_file.read())
        # print(wb)
        duplicates = wb[wb.duplicated()]  #dataframe for showing duplicate entries
        num_duplicates = duplicates.shape[0]

        # parsing the DataFrame in json format.
        json_records = duplicates.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {"something": True, "num_duplicates": num_duplicates, "duplicates_df": data}

        wb_without_duplicates = wb.drop_duplicates() #new dataframe
        
        return render(request, "index.html", context)
        
        # document = FilesUpload.objects.create(file = excel_file)
        # document.save()
        # return HttpResponse("FILE UPLOADED")
    else:
        return render(request, "index.html")

    return render(request, "index.html", context)

def upload(request):
    return render(request, "upload.html")