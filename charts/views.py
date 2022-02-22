from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django import template
# from home.models import User
from .models import StoreData
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncDate
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator


# @login_required
def mydashboard(request):
    context={}
    # dt = StoreData.objects.filter(naam=request.user).order_by('-id')[:10]
    # if dt.exists():
    weekly = StoreData.objects.annotate(week=TruncWeek('date')).values('week').annotate(AmtW=Count('date')).values('week','AmtW')
    snapWeek = round(weekly.latest('week')['AmtW'],0)

    monthly = StoreData.objects.annotate(month=TruncMonth('date')).values('month').annotate(AmtM=Count('date')).values('month','AmtM')
    snapMonth = round(monthly.latest('month')['AmtM'],0)

    yearly = StoreData.objects.annotate(year=TruncYear('date')).values('year').annotate(AmtY=Count('date')).values('year','AmtY')
    snapYear = round(yearly.latest('year')['AmtY'],0)
    context = {'weekly': weekly ,'monthly': monthly, 'yearly': yearly, 'snapWeek': snapWeek, 'snapMonth':snapMonth, 'snapYear':snapYear}

        # context = {'weekly': (0,0) ,'monthly': (0,0), 'yearly': (0,0), 'snapWeek': 0, 'snapMonth':0, 'snapYear':0}
    return render(request, "index.html", context)
