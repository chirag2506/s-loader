from django.shortcuts import render, redirect
from django.template import loader
# from django.http import HttpResponse
from django import template
from duplicate.models import FilesUpload
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncDate
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
# from django.http.response import JsonResponse
# from djqscsv import render_to_csv_response
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# Create your views here.


# @login_required(login_url="/login/")
# def mydashboard(request):
    # total = StoreData.objects.annotate(total=Count('date')).values('total')
    # context={}
    # weekly = FilesUpload.objects.annotate(week=TruncWeek('date')).values('week').annotate(AmtW=Count('date')).values('week','AmtW')
    # snapWeek = round(weekly.latest('week')['AmtW'],0)

    # monthly = FilesUpload.objects.annotate(month=TruncMonth('date')).values('month').annotate(AmtM=Count('date')).values('month','AmtM')
    # snapMonth = round(monthly.latest('month')['AmtM'],0)

    # yearly = FilesUpload.objects.annotate(year=TruncYear('date')).values('year').annotate(AmtY=Count('date')).values('year','AmtY')
    # snapYear = round(yearly.latest('year')['AmtY'],0)
    # context = {'weekly': weekly ,'monthly': monthly, 'yearly': yearly, 'snapWeek': snapWeek, 'snapMonth':snapMonth, 'snapYear':snapYear,}
    # return render(request, "index.html", context)

# def charts(request):
#     return render(request,'home.html')


def dashboard(request):
    spath = "/Users/HP/projects/s-loader/grouping/static/"
    print("path =", spath)
    temp_file=os.walk(spath)
    items={}
    operations = ["Counting duplicate rows", "Counting null rows", "Number of rows", "Number of Columns"]
    for root, directories, files in temp_file:
        for file in files:
            print("file path: ", spath+file)
            df = pd.read_excel(spath+file)
            # finding duplicate
            duplicates = df[df.duplicated()] 
            num_duplicates = duplicates.shape[0]
            try:
                items["Counting duplicate rows"].append({
                    'file_name': file,
                    'num_dup': num_duplicates
                })
            except:
                items["Counting duplicate rows"] = [{'file_name': file, 'num_dup': num_duplicates}]

            #finding number of rows having null value
            null_rows = df.isnull().sum()
            try:
                items["Counting null rows"].append({
                    'file_name': file,
                    'null_rows': num_rows
                })
            except:
                items["Counting null rows"] = [{'file_name': file, 'null_rows': null_rows}]

            # number of rows
            num_rows = df.shape[0]
            try:
                items["Number of rows"].append({
                    'file_name': file,
                    'num_rows': num_rows
                })
            except:
                items["Number of rows"] = [{'file_name': file, 'num_rows': num_rows}]

            # number of columns
            num_cols = df.shape[1]
            try:
                items["Number of Columns"].append({
                    'file_name': file,
                    'num_cols': num_cols
                })
            except:
                items["Number of Columns"] = [{'file_name': file, 'num_cols': num_cols}]

    print("items: ", items)
    context = {}
    context["dup_graph"] = plot_bar(items["Counting duplicate rows"])
    context["dup_graph1"] = plot_bar1(items["Counting null rows"])
    context["dup_graph2"] = plot_bar2(items["Number of rows"])
    context["dup_graph3"] = plot_bar3(items["Number of Columns"])
    print("context: ", context)
    return render(request, "charts.html", {'context': context})


def plot_bar(l: list):
    x = []
    y = []

    for record in l:
        print(record)
        x.append(record['file_name'])
        y.append(record['num_dup'])
    return {'labels': x, 'num_dup': y}

def plot_bar1(l: list):
    x = []
    y = []

    for record in l:
        print(record)
        x.append(record['file_name'])
        y.append(record['null_rows'])
    return {'labels': x, 'null_rows': y}


def plot_bar2(l: list):
    x = []
    y = []

    for record in l:
        print(record)
        x.append(record['file_name'])
        y.append(record['num_rows'])
    return {'labels': x, 'num_rows': y}


def plot_bar3(l: list):
    x = []
    y = []

    for record in l:
        print(record)
        x.append(record['file_name'])
        y.append(record['num_cols'])
    return {'labels': x, 'num_cols': y}