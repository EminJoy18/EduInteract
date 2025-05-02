import requests
import base64
from litellm import completion
import litellm
import os
from mistralai import Mistral

def text_extraction(image_path):
    os.environ["GEMINI_API_KEY"] = "AIzaSyBOk6ym1KApca-30KQtKRXJNTTSdNXF0G4"
    litellm.set_verbose = False

    # Path to the local image you want to upload
    image_path = f'{image_path}'


    # Read the image file and encode it as base64
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the payload
    response = completion(
        model = "gemini/gemini-1.5-pro-latest",
        messages = [
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": "Extract the text elements described by the user from the picture, and return the result formatted as a json in the following format : {name_of_element : [value]}"
                    },
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '''From this Computer Engineering Syllabus, extract the Module number, unit number and topics,
                        where topics are separated by commas present them as a list and return it as a JSON String.
                        The overall JSON file must follow the format:
                        {
                        Module Number: <module_number>,
                        Module Name: <module_name>,
                        Subtopics: [
                            {
                            Unit Number: <unit_number>,
                            Topics: [<topic1>, <topic2>, ...]
                            },
                        Hrs(which refers to the number of recommended hours to finish the syllabus)
                        }
                        It must be a single JSON file, such that it gives me no JSONDecodeError.
                        I have zero tolerances to error, so make sure that the text scanned is accurate in units.'''
                    },
                    {
                        "type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}"
                    }
                ]
            }
        ],
        response_format = {"type": "json_object"}
    )

    result = response['choices'][0]['message']['content']


    # Converting to json
    model = "mistral-large-latest"

    client = Mistral(api_key='BZKpd0qBpZuiMlzgrJ7brNdPlkOXiX9x')
    messages = [
        {
            "role": "user",
            "content": f"Read {result}, and make sense of it. Present it in a JSON Format. I need only the document, no other descriptions.",
        }
    ]
    chat_response = client.chat.complete(
        model = model,
        messages = messages,
        response_format = {
            "type": "json_object",
        },
        safe_prompt = True
    )

    syllabus = chat_response.choices[0].message.content


    return(syllabus)