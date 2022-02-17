from csv import excel
from urllib import request
from django.shortcuts import render, HttpResponse
from .models import FilesUpload
import pandas as pd
from .forms import uploadform
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
def home(request):
    if request.method == "POST":
        path = os.environ["PATH"]
        temp_file=os.walk(path)
        columns=[]
        rows=[]
        num_duplicates=[]
        num_tables=0
        context=[]
        for root, directories, files in temp_file:
            for file in files:
                df=pd.read_excel(path+file)
                duplicates = df[df.duplicated()] 
                num_duplicates.append(duplicates.shape[0])
                columns.append(list(duplicates.columns))
                rows.append(duplicates.values[:,:])
                num_tables+=1
                context.append({
                    'num_duplicates':duplicates.shape[0],
                    'columns':list(duplicates.columns),
                    'rows':duplicates.values[:,:],
                })
        print('duplicates',num_duplicates)
        
        return render(request, "index1.html", {'context': context})
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
    