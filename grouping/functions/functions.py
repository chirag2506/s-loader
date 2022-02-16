import pandas as pd
import csv
from io import BufferedReader
def handle_uploaded_file(f):
    with open('grouping/static/'+f.name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return destination


def get_fields(f):
   df=pd.read_excel(f.name)
   #print(list(df.columns))
   return list(df.columns)
