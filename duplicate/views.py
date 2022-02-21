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
    spath = "/Users/drumilshah/Documents/S-Loader/s-loader/grouping/static/"
    print("path =", spath)
    temp_file=os.walk(spath)
    columns=[]
    rows=[]
    num_duplicates=[]
    num_tables=0
    context=[]
    for root, directories, files in temp_file:
        for file in files:
            print("file path: ", spath+file)
            df=pd.read_excel(spath+file)
            duplicates = df[df.duplicated()] 
            num_duplicates.append(duplicates.shape[0])
            columns.append(list(duplicates.columns))
            rows.append(duplicates.values[:,:])
            num_tables+=1
            context.append({
                "file_name": file,
                'num_duplicates':duplicates.shape[0],
                'columns':list(duplicates.columns),
                'rows':duplicates.values[:,:],
            })
    print('duplicates',num_duplicates)
    return render(request, "duplicate.html", {'context': context})

def upload(request):
    return render(request, "upload.html")
    