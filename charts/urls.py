from django.urls import path, re_path
from . import views


urlpatterns = [
    path('dashboard', views.mydashboard, name='dashboard')
    # path('view_data', views.tableOfData, name='blog-tableOfData'),
]
