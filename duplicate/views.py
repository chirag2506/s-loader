from csv import excel
from urllib import request
from django.shortcuts import render, HttpResponse
from .models import FilesUpload
import pandas as pd
import pip
# pip.main(["install", "openpyxl"])
import json
from .forms import uploadform


# Create your views here.
def home(request):
    if request.method == "POST":

        # user=uploadform(request.POST,request.FILES)
        # files = request.FILES.getlist('files')

        excel_file = request.FILES["myFile"]
        wb = pd.read_excel(excel_file.read())

        json_wb = wb.to_json()
        request.session['wb'] = json_wb #saving workbook in session

        # print(wb)
        duplicates = wb[wb.duplicated()]  #dataframe for showing duplicate entries
        num_duplicates = duplicates.shape[0]

        columns_head = duplicates.columns
        rows = duplicates.values[:,:]

        # parsing the DataFrame in json format.
        # json_records = duplicates.reset_index().to_json(orient ='records')
        # data = []
        # data = json.loads(json_records)
        context = {"something": True, "num_duplicates": num_duplicates, "df_columns": columns_head,"duplicates_df": rows}

        wb_without_duplicates = wb.drop_duplicates() #new dataframe without duplicates
        
        return render(request, "index1.html", context)
        
        # document = FilesUpload.objects.create(file = excel_file)
        # document.save()
        # return HttpResponse("FILE UPLOADED")
    else:
        return render(request, "index1.html")

def upload(request):
    return render(request, "upload.html")

def group(request):
    df = request.session.get('wb', None)
    df = pd.read_json(df)

    if 'delete_dup' in request.POST:
        wb_without_duplicates = df.drop_duplicates()
        columns_head = wb_without_duplicates.columns
        rows = wb_without_duplicates.values[:,:]

        context_next = {"something": True, "df_columns": columns_head,"df_rows": rows}

        return render(request, "grouping.html", context_next)

    elif 'keep_dup' in request.POST:
        columns_head = df.columns
        rows = df.values[:,:]

        context_next = {"something": True, "df_columns": columns_head,"df_rows": rows}

        return render(request, "grouping.html", context_next)

    else:
        return render(request, "grouping.html")
    