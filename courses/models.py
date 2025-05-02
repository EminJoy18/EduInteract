from django.db import models
import json
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

DEPARTMENT_CHOICES = [
        ('Computer Engineering', 'Computer Engineering'),
        ('Artificial Intelligence and Data Science', 'Artificial Intelligence and Data Science'),
        ('Electronics and Computer Science', 'Electronics and Computer Science'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
    ]

class Course(models.Model):
    CourseID = models.CharField(max_length=20, unique=True, primary_key=True)
    Course_Name = models.CharField(max_length=255)
    Semester = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ])
    Department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    Syllabus_source = models.ImageField(upload_to='syllabus_images/', null=True, blank=True)
    Syllabus = models.JSONField(null=True, blank=True)
    # Course_Outcomes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.Course_Name