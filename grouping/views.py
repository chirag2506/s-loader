from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
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
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())
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
            return redirect('/home')
        if len(files)==0:
            messages.success(request, "Please select a file" )
            return redirect('/home')
        for i in files:
            if i.name[-4:]!='xlsx':
                messages.success(request, "Please upload files in xlsx format" )
                return redirect('/home')

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
            fields.append([request.POST.getlist(i),i[:-7]])
        fields=fields[1:-1]
        fields=sorted(fields,key=lambda x: (x[1]))
        s_path = os.environ['SYS_PATH']
        path = os.walk(s_path)
        files_path=[]
        file_name=[]
        for root, directories, files in path:
            for file in files:
                file_name.append(file)
                files_path.append(os.path.join(s_path,file))
        # print(files_path)
        connectionUri = os.environ['DB_CONNECTION_URI']
        engine = create_engine(connectionUri)
        x=0
        for i,j in zip(files_path,fields):
            df=pd.read_excel(i)
            df = df[j[0]]
            df.to_excel(i,index=False)
            df['date']=datetime.today().strftime('%Y-%m-%d')
            t=engine.table_names()
            if file_name[x] not in t:
                print(file_name[x])
                df.to_sql(file_name[x], con=engine)
            else:
                c=file_name[x]+str(random.randint(0,9))
                while c in t:
                    c+=str(random.randint(0,9))
                df.to_sql(c, con=engine)
            os.remove(i)

            x+=1
        messages.success(request, "Grouping completed!", extra_tags="uploaded")
        return redirect('/duplicate/')

    else:
        return render(request, "home.html")
