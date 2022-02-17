from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.selcol,name='multiple'),
    path('select_columns', views.select, name='select_columns'),
    path('column_process', views.column_pro, name='column_pro' )
]
