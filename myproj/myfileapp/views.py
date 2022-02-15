from django.shortcuts import render
import openpyxl
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from myfileapp.forms import uploadform
from django.contrib import messages
from .models import myuploadfile

def index(request):
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        user=uploadform(request.POST,request.FILES)
        context={}
        excel_file = request.FILES.getlist("excel_file")
        
        '''if len(excel_file)>5:
             context={'msg':'<span style="color:black;">please upload 5 files at max</span>'}
             return render(request,"index.html",context)'''
        wb=pd.read_excel(excel_file.read())
        '''if not excel_file.name.endswith('xlsx'or 'xls'):
             messages.info(request,'Sorry Wrong File Format.Please Upload valid format')
             return render(request,'index.html')'''
        # you may put validations here to check extension or file size
        print(excel_file)
        wb = openpyxl.load_workbook(excel_file)
        
        # getting a particular sheet by name out of many sheets
       
       
        
        engine = create_engine('mysql://root:@127.0.0.1/data')
        wb.to_sql(excel_file.name, con = engine)
        #print(worksheet)
        excel_data=wb.to_dict()
        
        
        
        

        return render(request, 'index.html', {"excel_data":excel_data})
