from django.shortcuts import render, redirect
from django.template import loader
# from django.http import HttpResponse
from django import template
from .models import StoreData
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncDate
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
# from django.http.response import JsonResponse
# from djqscsv import render_to_csv_response

# Create your views here.




# @login_required(login_url="/login/")
def mydashboard(request):
    # total = StoreData.objects.annotate(total=Count('date')).values('total')
    context={}
    weekly = StoreData.objects.annotate(week=TruncWeek('date')).values('week').annotate(AmtW=Count('date')).values('week','AmtW')
    snapWeek = round(weekly.latest('week')['AmtW'],0)

    monthly = StoreData.objects.annotate(month=TruncMonth('date')).values('month').annotate(AmtM=Count('date')).values('month','AmtM')
    snapMonth = round(monthly.latest('month')['AmtM'],0)

    yearly = StoreData.objects.annotate(year=TruncYear('date')).values('year').annotate(AmtY=Count('date')).values('year','AmtY')
    snapYear = round(yearly.latest('year')['AmtY'],0)
    context = {'weekly': weekly ,'monthly': monthly, 'yearly': yearly, 'snapWeek': snapWeek, 'snapMonth':snapMonth, 'snapYear':snapYear,}
    return render(request, "index.html", context)
