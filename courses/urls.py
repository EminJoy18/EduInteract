from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.subject, name='upload_syllabus'),
    path('syllabus_extract/', views.syllabus_extract, name='syllabus_extract'),
    path('view_uploaded/', views.view_uploaded, name='view_uploaded'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)