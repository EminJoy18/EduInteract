from django.shortcuts import render, get_object_or_404
from courses.models import Course
from django.http import JsonResponse
from .generate_mcq_questions import generate_mcqs
import json
from .text_cleaner import cleaner
from .google_form_template_generator import template_generator
from datetime import datetime
from django.contrib import messages
from .automating_google_form import automated_google_form_generation
from .generate_lesson_plan import lesson_plan

mcq_questions = str()
subject = str()

# Create your views here.
def question_paper_generation(request):
    courses = Course.objects.all()
    context = {
        'courses' : courses,
    }
    return render(request, 'question_paper.html', context)


def generate_questions(request):
    if request.method == 'POST':
        global subject 
        subject = selected_subject = request.POST.get('subject')
        selected_modules = request.POST.getlist('modules')
        no_of_questions = request.POST.get('no_of_questions')

        try:
            course = Course.objects.get(CourseID=selected_subject)
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)

        selected_modules_lst = []

        for module in selected_modules:
            selected_modules_lst.append(module)
            print(f"Module selected: {module}")

        # print(f"Selected Modules: {', '.join(selected_modules_str)}")

        mcq_questions = generate_mcqs(course.Syllabus, selected_modules_lst, no_of_questions)
        # mcq_questions = [
            # {
            #     "Serial no": 1,
            #     "Question": "Which of the following is not a type of Machine Learning?",
            #     "Options": [
            #         "Supervised Learning",
            #         "Unsupervised Learning",
            #         "Reinforcement Learning",
            #         "Binary Learning"
            #     ],
            #     "Answer": "Binary Learning",
            #     "Module": "Module1"
            # },
            # {
            #     "Serial no": 2,
            #     "Question": "What is the primary issue addressed by the Bias-Variance trade-off?",
            #     "Options": [
            #         "Underfitting and Overfitting",
            #         "Training and Testing Error",
            #         "Accuracy and Precision",
            #         "Data Cleaning and Preprocessing"
            #     ],
            #     "Answer": "Underfitting and Overfitting",
            #     "Module": "Module1"
            # },
            # {
            #     "Serial no": 3,
            #     "Question": "Which of the following is a disadvantage of Multivariate Linear Regression?",
            #     "Options": [
            #         "It handles multiple input variables",
            #         "It can model complex relationships",
            #         "It can lead to multicollinearity",
            #         "It always provides accurate predictions"
            #     ],
            #     "Answer": "It can lead to multicollinearity",
            #     "Module": "Module2"
            # },
            # {
            #     "Serial no": 4,
            #     "Question": "What does the Gini Index measure in the context of Decision Trees?",
            #     "Options": [
            #         "The variance of the data",
            #         "The impurity of the data",
            #         "The accuracy of the model",
            #         "The number of splits"
            #     ],
            #     "Answer": "The impurity of the data",
            #     "Module": "Module2"
            # },
            # {
            #     "Serial no": 5,
            #     "Question": "Which performance metric is used to evaluate the performance of a binary classifier?",
            #     "Options": [
            #         "Confusion Matrix",
            #         "Kappa Statistics",
            #         "Sensitivity",
            #         "All of the above"
            #     ],
            #     "Answer": "All of the above",
            #     "Module": "Module2"
            # },
            # {
            #     "Serial no": 6,
            #     "Question": "What is the primary purpose of K-fold cross-validation?",
            #     "Options": [
            #         "To split the data into training and testing sets",
            #         "To evaluate the model's performance on different subsets of the data",
            #         "To increase the model's complexity",
            #         "To reduce the number of features"
            #     ],
            #     "Answer": "To evaluate the model's performance on different subsets of the data",
            #     "Module": "Module3"
            # },
            # {
            #     "Serial no": 7,
            #     "Question": "Which of the following is a type of Boosting algorithm?",
            #     "Options": [
            #         "K-Nearest Neighbors",
            #         "XGBoost",
            #         "Principal Component Analysis",
            #         "Linear Regression"
            #     ],
            #     "Answer": "XGBoost",
            #     "Module": "Module3"
            # },
            # {
            #     "Serial no": 8,
            #     "Question": "What is the fundamental idea behind Bagging?",
            #     "Options": [
            #         "Combining weak learners sequentially",
            #         "Combining multiple models to reduce variance",
            #         "Reducing the dimensionality of the data",
            #         "Increasing the bias of the model"
            #     ],
            #     "Answer": "Combining multiple models to reduce variance",
            #     "Module": "Module3"
            # },
            # {
            #     "Serial no": 9,
            #     "Question": "Which of the following is a disadvantage of Random Forest?",
            #     "Options": [
            #         "It can handle a large number of input variables",
            #         "It is prone to overfitting",
            #         "It can handle both classification and regression tasks",
            #         "It is less interpretable"
            #     ],
            #     "Answer": "It is less interpretable",
            #     "Module": "Module3"
            # },
            # {
            #     "Serial no": 10,
            #     "Question": "What is the key difference between Boosting and Bagging?",
            #     "Options": [
            #         "Boosting combines weak learners sequentially, while Bagging combines them in parallel",
            #         "Boosting reduces variance, while Bagging reduces bias",
            #         "Boosting is used for classification, while Bagging is used for regression",
            #         "Boosting and Bagging are the same"
            #     ],
            #     "Answer": "Boosting combines weak learners sequentially, while Bagging combines them in parallel",
            #     "Module": "Module3"
            # }
            #     ]

        quill_content = ""

        for question in mcq_questions:
            quill_content += f"<p class='question' style='font-size: 18px; margin-bottom: 20px;'><strong>{question['Question']}</strong></p>"
            for option in question['Options']:
                quill_content += f"<p class='option' style='font-size: 18px; margin-left: 20px;'>{option}</p>"
            quill_content += f"<p class='answer' style='font-size: 18px; margin-top: 10px; color: green;'><strong>Answer: {question['Answer']}</strong></p><br>"
            quill_content += f"<p class='module' style='font-size: 18px; margin-top: 10px;'><strong>Module: {question['Module']}</strong></p><br>"

        return render(request, 'generate_form.html', {
            'course': course,
            'numbers': range(1,7),
            'selected_modules': selected_modules_lst,
            'quill_content' : quill_content,
        })
    

    courses = Course.objects.all()
    context = {
        'courses' : courses,
        'numbers' : range(1,7),
    }
    return render(request, 'generate_form.html', context)


def generate_google_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            raw_text = data.get("quill_content", "").strip()
            # print(raw_text)
            mcq_questions = cleaner(raw_text) # to clean the raw text
            # mcq_questions = raw_text
            questions_for_form = list()
            # print("Cleaned Questions:", mcq_questions)
            questions_for_form = template_generator(mcq_questions) # to fit the questions in the format
            # print("Generated Form Questions:", questions_for_form)
            print(len(questions_for_form))
            # generating the form
            if automated_google_form_generation(questions_for_form, subject):
                messages.success(request, "Google Form saved successfully!")
                return render(request, 'generate_form.html')
            else:
                messages.error(request, "Google Form could not be saved successfully!")
                return render(request, 'generate_form.html')

            # return JsonResponse({"success": True, "message": "Content saved successfully!"})

        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": "Failed to save content."})

    return JsonResponse({"success": False, "message": "Invalid request."})



def generate_lesson_plan(request):
    if request.method == 'POST':
        course_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        course = get_object_or_404(Course, CourseID=course_id)
        syllabus_json = course.Syllabus
        lp = lesson_plan(syllabus_json, start_date, end_date)

        quill_content = ""
        for week in lp:
            quill_content += f"<p style='font-size: 18px;'> Week Number: <strong>{week.get('week_number', 'N/A')}</strong></p>"
            
            # Topics
            quill_content += f"<p style='font-size: 18px;'><strong>Topics:</strong></p><ul>"
            for topic in week['topics']:
                quill_content += f"<li>{topic}</li>"
            quill_content += "</ul>"

            # Practical Lab Aim
            quill_content += f"<p style='font-size: 18px;'><strong>Practical Lab <br>Aim: </strong>{week['practical_lab']['aim']}</p>"

            # Practical Lab Objectives
            quill_content += f"<p style='font-size: 18px;'><strong>Objectives:</strong><ul>"
            for objective in week['practical_lab']['objectives']:
                quill_content += f"<li>{objective}</li>"
            quill_content += "</ul></p>"

        print(lp)
        return render(request, 'lesson_plan.html', {
            # 'lesson_plan': lp,
            'quill_content' : quill_content,
        })
    
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }    
    return render(request, 'lesson_plan.html', context)