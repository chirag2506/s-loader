from csv import excel
from urllib import request
from django.shortcuts import render, HttpResponse
from .models import FilesUpload
import pandas as pd
import pip
# pip.main(["install", "openpyxl"])
import json
from .forms import uploadform
import os

# Create your views here.
def home(request):
    if request.method == "POST":

        # user=uploadform(request.POST,request.FILES)
        # files = request.FILES.getlist('files')
        temp_file=os.walk('/Users/HP/projects/s-loader/grouping/static')
        columns=[]
        rows=[]
        num_duplicates=[]
        num_tables=0
        context={}
        for root, directories, files in temp_file:
            for file in files:
                df=pd.read_excel('/Users/HP/projects/s-loader/grouping/static/'+file)
                duplicates = df[df.duplicated()]  #dataframe for showing duplicate entries
                num_duplicates.append(duplicates.shape[0])
                columns.append(list(duplicates.columns))
                rows.append(duplicates.values[:,:])
                num_tables+=1
                context['table'+str(num_tables)]={
                    'num_duplicates':duplicates.shape[0],
                    'columns':list(duplicates.columns),
                    'rows':duplicates.values[:,:],
                }

        print('duplicates',num_duplicates)
        # parsing the DataFrame in json format.
        # json_records = duplicates.reset_index().to_json(orient ='records')
        # data = []
        # data = json.loads(json_records)
        print(context)
        wb_without_duplicates = df.drop_duplicates() #new dataframe without duplicates
        
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
    