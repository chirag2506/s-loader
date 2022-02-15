from django.shortcuts import render
from django.http import HttpResponse
from grouping.functions.functions import get_fields,handle_uploaded_file
from grouping.forms import uploadform
import os
from pathlib import Path
import pandas as pd
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import random
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent
def selcol(request):
    return render(request, 'multiple.html')

def select(request):
    if request.method=='POST':
        user=uploadform(request.POST,request.FILES)
        files = request.FILES.getlist('files')
        context={}
        if len(files)>5:
            messages.success(request, "Please upload 5 files at max" )
            return render(request, "multiple.html")
        if user.is_valid():
            i=0
            for f in files:
                t=handle_uploaded_file(f)
                cols=get_fields(t)
                i+=1
                context[f.name]=cols
            con={
                'context':context
            }
            #print(con)
            return render(request, "select_columns.html",con)
    else:
        user=uploadform()
    return render(request, "select_columns.html")

def column_pro(request):
    if request.method=='POST':
        fields=[]
        t=request.POST
        for i in t:
            fields.append(request.POST.getlist(i))
        fields=fields[1:-1]
        path = os.walk(os.path.join(BASE_DIR,'grouping\static'))
        files_path=[]
        file_name=[]
        for root, directories, files in path:
            for file in files:
                file_name.append(file)
                files_path.append(os.path.join(os.path.join(BASE_DIR,'grouping\static'),file))
        engine = create_engine('mysql://uaf9zenjb3zwdszd:MOTaVWWxUIT6MOPCXNU0@bldot2uujx3isi3clafh-mysql.services.clever-cloud.com:3306/bldot2uujx3isi3clafh')
        x=0
        for i,j in zip(files_path,fields):
            df=pd.read_csv(i)
            df = df[j]
            t=engine.table_names()
            if file_name[x] not in t:
                df.to_sql(file_name[x], con=engine)
            else:
                c=file_name[x]+str(random.randint(0,9))
                while c in t:
                    c+=str(random.randint(0,9))
                df.to_sql(c, con=engine)
            os.remove(i)
            x+=1
            
        return render(request, "multiple.html")
    else:
        return render(request, "multiple.html")