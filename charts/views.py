from django.shortcuts import render,redirect
import os
import pandas as pd
from django.views.decorators.cache import cache_control
from .models import StoreData
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek
from django.db.models import Count

def dashboard(request):
    spath = os.environ['SYS_PATH']
    temp_file=os.walk(spath)
    items={}
    operations = ["Counting duplicate rows", "Counting null rows", "Number of rows", "Number of Columns"]
    for root, directories, files in temp_file:
        for file in files:
            df = pd.read_excel(spath+file)
            duplicates = df[df.duplicated()] 
            num_duplicates = duplicates.shape[0]
            try:
                items["Counting duplicate rows"].append({
                    'file_name': file,
                    'num_dup': num_duplicates
                })
            except:
                items["Counting duplicate rows"] = [{'file_name': file, 'num_dup': num_duplicates}]

            null_rows = df.isnull().any(axis=1).sum()
            try:
                items["Counting null rows"].append({
                    'file_name': file,
                    'null_rows': null_rows
                })
            except:
                items["Counting null rows"] = [{'file_name': file, 'null_rows': null_rows}]
            
            null_cols = df.isna().sum()
            try:
                items["Counting null columns"].append({
                    'file_name': file,
                    'null_cols': null_cols
                })
            except:
                items["Counting null columns"] = [{'file_name': file, 'null_cols': null_cols}]

            num_rows = df.shape[0]
            
            try:
                items["Number of rows"].append({
                    'file_name': file,
                    'num_rows': num_rows
                })
            except:
                items["Number of rows"] = [{'file_name': file, 'num_rows': num_rows}]
            num_cols = df.shape[1]
            try:
                items["Number of Columns"].append({
                    'file_name': file,
                    'num_cols': num_cols
                })
            except:
                items["Number of Columns"] = [{'file_name': file, 'num_cols': num_cols}]
    context = {}
    context["dup_graph"] = plot_bar(items["Counting duplicate rows"])
    context["dup_graph1"] = plot_bar1(items["Counting null rows"])
    context["dup_graph2"] = plot_bar2(items["Number of rows"])
    context["dup_graph3"] = plot_bar3(items["Number of Columns"])
    context["dup_graph4"] = plotPie(items["Counting null columns"])
    
    return render(request, "charts.html", {'context': context})


def plot_bar(l: list):
    x = []
    y = []

    for record in l:
        if len(record['file_name'])>5:
            record['file_name']=record['file_name'][:5]
        x.append(record['file_name'])
        y.append(record['num_dup'])
    return {'labels': x, 'num_dup': y}

def plot_bar1(l: list):
    x = []
    y = []

    for record in l:
        if len(record['file_name'])>5:
            record['file_name']=record['file_name'][:5]
        x.append(record['file_name'])
        y.append(record['null_rows'])
    return {'labels': x, 'null_rows': y}


def plot_bar2(l: list):
    x = []
    y = []

    for record in l:
        if len(record['file_name'])>5:
            record['file_name']=record['file_name'][:5]
        x.append(record['file_name'])
        y.append(record['num_rows'])
    return {'labels': x, 'num_rows': y}


def plot_bar3(l: list):
    x = []
    y = []

    for record in l:
        if len(record['file_name'])>5:
            record['file_name']=record['file_name'][:5]
        x.append(record['file_name'])
        y.append(record['num_cols'])
    return {'labels': x, 'num_cols': y}

def plotPie(l: list):
    dict={}
    for record in l:
        dict[record['file_name']]={'value':record['null_cols'].tolist(),'ind':list(record['null_cols'].index)}
    return dict

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def finish(request):
    spath = os.environ['SYS_PATH']
    temp_file=os.walk(spath)
    
    for root, directories, files in temp_file:
        for file in files:
            os.remove(spath+file)
    return redirect('/home')

def mydashboard(request):
    context={}
    dt = StoreData.objects.filter(naam=request.session.get('username')).order_by('-id')[:10]
    if dt.exists():
        weekly = StoreData.objects.filter(naam=request.session.get('username')).annotate(week=TruncWeek('date')).values('week').annotate(AmtW=Count('date')).values('week','AmtW')
        snapWeek = round(weekly.latest('week')['AmtW'],0)

        monthly = StoreData.objects.filter(naam=request.session.get('username')).annotate(month=TruncMonth('date')).values('month').annotate(AmtM=Count('date')).values('month','AmtM')
        snapMonth = round(monthly.latest('month')['AmtM'],0)

        yearly = StoreData.objects.filter(naam=request.session.get('username')).annotate(year=TruncYear('date')).values('year').annotate(AmtY=Count('date')).values('year','AmtY')
        snapYear = round(yearly.latest('year')['AmtY'],0)
        context = {'weekly': weekly ,'monthly': monthly, 'yearly': yearly, 'snapWeek': snapWeek, 'snapMonth':snapMonth, 'snapYear':snapYear}
    else:
        context = {'weekly': (0,0) ,'monthly': (0,0), 'yearly': (0,0), 'snapWeek': 0, 'snapMonth':0, 'snapYear':0}
    return render(request, "index.html", context)