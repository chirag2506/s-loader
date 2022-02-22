from django.shortcuts import render,redirect
import os
import pandas as pd
from django.views.decorators.cache import cache_control

def dashboard(request):
    spath = "/Users/HP/projects/s-loader/grouping/static/"
    temp_file=os.walk(spath)
    items={}
    operations = ["Counting duplicate rows", "Counting null rows", "Number of rows", "Number of Columns"]
    for root, directories, files in temp_file:
        for file in files:
            print("file path: ", spath+file)
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
    context["dup_graph4"] = plot_bar4(items["Counting null columns"])
    
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

def plot_bar4(l: list):
    dict={}
    for record in l:
        dict[record['file_name']]={'value':record['null_cols'].tolist(),'ind':list(record['null_cols'].index)}
    return dict

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def finish(request):
    return redirect('/home')