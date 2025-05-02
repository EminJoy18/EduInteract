from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account key file
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
form = {
    "info": {
        "title": "ML_ISE2_11-11-2024",
        "documentTitle": "ML_ISE2_11-11-2024"
    }
}

# Step 1: Create the form with only the title
try:
    form_response = forms_service.forms().create(body=form).execute()
    form_id = form_response['formId']
    print(f'Form created successfully! Form ID: {form_id}')
except Exception as e:
    print("An error occurred while creating the form:", e)
    form_id = None

# Step 2: Add questions to the form using batchUpdate
if form_id:
    requests = [
        {
            "createItem": {
                "item": {
                    "title": "Name",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False  # Short answer type
                            }
                        }
                    }
                },
                "location": {
                    "index": 0
                }
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Roll No.",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False  # Short answer type
                            }
                        }
                    }
                },
                "location": {
                    "index": 1
                }
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Class",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",  # Multiple choice question
                                "options": [
                                    {"value": "BE COMPS A"},
                                    {"value": "BE COMPS B"}
                                ],
                                "shuffle": False
                            }
                        }
                    }
                },
                "location": {
                    "index": 2
                }
            }
        }
    ]

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
        'emailAddress': 'crce.9546.ce@gmail.com'  # Replace with your personal Google account email
    }

    try:
        drive_service.permissions().create(
            fileId=form_id,
            body=permissions_body,
            fields='id'
        ).execute()
        print("Form shared successfully with your account!")
    except Exception as e:
        print("An error occurred while sharing the form:", e)