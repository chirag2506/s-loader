from django.urls import path, re_path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard')
    # path('view_data', views.tableOfData, name='blog-tableOfData'),
]
