from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home,name='dupli_index'),
    path('upload/', views.upload,name='upload'),
    path('grouping/', views.group)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
