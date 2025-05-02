from google.oauth2 import service_account
from googleapiclient.discovery import build
from courses.models import Course
from datetime import datetime

def automated_google_form_generation(questions_for_form, subject):
    # generating the google form by passing the questions
    SERVICE_ACCOUNT_FILE = 'majestic-camp-441316-a8-75d9db2da70b.json'

    # Scopes for the Google Forms and Drive APIs
    SCOPES = [
        'https://www.googleapis.com/auth/forms.body',
        'https://www.googleapis.com/auth/drive'
    ]

    # Initialize the credentials and services
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    forms_service = build('forms', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Define the form title only
    course = Course.objects.get(CourseID=subject)
    form = {
        "info": {
            "title": f"{course}_{datetime.today().strftime('%d-%m-%Y')}_Quiz",
            "documentTitle": f"{course}_{datetime.today().strftime('%d-%m-%Y')}_Quiz"
            # "title": f"Quiz",
            # "documentTitle": f"Quiz"
        }
    }

    try:
        form_response = forms_service.forms().create(body=form).execute()
        form_id = form_response['formId']
        print(f'Form created successfully! Form ID: {form_id}')
    except Exception as e:
        print("An error occurred while creating the form:", e)
        form_id = None

    # Step 2: Add questions to the form using batchUpdate
    if form_id:
        try:
            quiz_request = {
                "requests": [
                    {
                        "updateSettings": {
                            "settings": {
                                "quizSettings": {
                                    "isQuiz": True  # Enable quiz mode
                                }
                            },
                            "updateMask": "quizSettings.isQuiz"
                        }
                    }
                ]
            }
            forms_service.forms().batchUpdate(formId=form_id, body=quiz_request).execute()
            print("Quiz settings enabled successfully!")
        except Exception as e:
            print("An error occurred while enabling quiz settings:", e)


    if form_id:
        requests = questions_for_form

        try:
            forms_service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
            print("Questions added successfully!")
        except Exception as e:
            print("An error occurred while adding questions:", e)

    # Step 3: Share the form with your Google account
    if form_id:
        permissions_body = {
            'role': 'writer',  # Use 'reader' for view-only access
            'type': 'user',
            'emailAddress': ''  # Replace with your personal Google account email
        }

        try:
            drive_service.permissions().create(
                fileId=form_id,
                body=permissions_body,
                fields='id'
            ).execute()
            print("Form shared successfully with your account!")
            return 1
        except Exception as e:
            print("An error occurred while sharing the form:", e)
            return 0
