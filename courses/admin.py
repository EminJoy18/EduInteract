from django.contrib import admin
from .models import Course
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['CourseID', 'Course_Name']

admin.site.register(Course, CourseAdmin)