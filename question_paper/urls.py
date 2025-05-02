from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.question_paper_generation, name='question_paper'),
    path('generate_questions', views.generate_questions, name='generate_questions'),
    path('generate_form', views.generate_google_form, name='generate_form'),
    path('generate_lesson_plan', views.generate_lesson_plan, name='generate_lesson_plan'),
]