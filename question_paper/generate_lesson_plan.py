from mistralai import Mistral
import json
from datetime import datetime

def lesson_plan(syllabus, start_date, end_date):
    # requirements for generating lesson plan
    syllabus = syllabus

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    week_difference = (end_date - start_date).days // 7

    model = "mistral-large-latest"
    client = Mistral(api_key='')
    messages = [
        {
                "role": "system",
                "content": "You are an expert Lesson Plan Generator, who is capable of generating Lesson Plans that strictly adhere to the context. The context is the syllabus for the subject."
        },
        {
            "role": "user",
            "content": f'''
                You are required to generate a Lesson Plan that strictly adheres to the context provided. Read, understand and reason with all the resources provided.
                The syllabus for the subject is - {syllabus}
                The lesson plan must be generated for the following dates: {start_date} to {end_date}.
                So the number of weeks essentially between this time period is {week_difference} weeks.
                The lesson plan must be structured in a way that it covers all the topics in the syllabus within the given dates.
                The lesson plan must be structured in a JSON format and include the following details:

            1. Week Number
            2. Dates of the week (start date and end date)
            3. Topics to be covered during the week
            4. Practical Lab Session:
                - Aim of the experiment
                - Objectives of the experiment

            The lesson plan must be designed to help the educator teach the course effectively and ensure that all topics in the syllabus are covered within the given dates. The practical lab sessions should help students apply the concepts learned during the week.
            You must make sure that the last week number should be equal to the {week_difference}.
            Segment the entire topics into a set of {week_difference} number of elements, so that way you won't lose the count of of the weeks. Because I can't afford any shortcomings
            Count through each week in the time period between {start_date} and {end_date}, so that it is easier to print the lesson plan in a structured way.

            Generate the lesson plan in the following list of dictionaries format:
            [
                dict(
                "week_number": <week_number>,
                "topics": ["Topic 1", "Topic 2", ...],
                "practical_lab": 
                    "aim": "Aim of the experiment",
                    "objectives": ["Objective 1", "Objective 2", ...]       
                ),
                ...
            ]
            ''',
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

    lesson_plan = chat_response.choices[0].message.content

    try:
        json_data = json.loads(lesson_plan)
        print("Corrected JSON data:")
        print(json.dumps(json_data, indent=4))
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    return json_data
