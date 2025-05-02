from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from .models import Course
from django.contrib import messages
from .text_extracter_from_image import text_extraction
import json
import os
from django.conf import settings

syllabus_json = str()
co_json = str()

# Create your views here.
def subject(request):
    if request.method == 'POST':
        image = request.FILES['syllabus_image']

        image_path = os.path.join(settings.MEDIA_ROOT, 'syllabus_images', image.name)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        
        # # Use Gemini for text extraction (assuming it has a method `extract_text_from_image`)
        # extracted_text = Gemini.extract_text_from_image(path)
        # syllabus_json = json.loads(extracted_text)  # Assuming extracted text can be converted to JSON

        # text extraction from syllabus
        syllabus = text_extraction(image_path)

        try:
            syllabus_json = json.loads(syllabus)
            # print("Corrected JSON data:")
            print(json.dumps(syllabus_json, indent=4))
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)


        # course_outcomes_json = 

        # Save JSON to the Syllabus field
        course = Course.objects.create(
            CourseID=request.POST['course_id'],
            Course_Name=request.POST['course_name'],
            Semester=request.POST['semester'],
            Department=request.POST['department'],
            
            Syllabus=syllabus_json,
            # Course_Outcomes=
        )
        course.save()

        # Remove temporary file
        # default_storage.delete(path)

        messages.success(request, "Course syllabus uploaded successfully!")
        return render(request, 'syllabus_upload.html', {'syllabus_json': syllabus_json})

    return render(request, 'syllabus_upload.html')



def syllabus_extract(request):
    if request.method == 'POST':
        image = request.FILES['syllabus_image']

        image_path = os.path.join(settings.MEDIA_ROOT, 'syllabus_images', image.name)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # text extraction from syllabus
        syllabus = text_extraction(image_path)

        try:
            syllabus_json = json.loads(syllabus)
            # print("Corrected JSON data:")
            # print(json.dumps(syllabus_json, indent=4))
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)

    return render(request, 'syllabus_upload.html', {'syllabus_json': syllabus_json})



def view_uploaded(request):
    if request.method == 'POST':
        course_id = request.POST.get('subject')

        if course_id:
            course = get_object_or_404(Course, CourseID=course_id)
            syllabus_json = course.Syllabus
            return render(request, 'view_uploaded.html', {
                'course': course,
                'syllabus_json': syllabus_json,
            })

    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'view_uploaded.html', context)