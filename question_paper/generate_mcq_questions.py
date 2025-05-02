import os
from mistralai import Mistral
import json

def generate_mcqs(syllabus, modules_list, number_of_questions):
    # requirements for generating question paper
    syllabus = syllabus
    # total_marks = 10

    model = "mistral-large-latest"
    client = Mistral(api_key='BZKpd0qBpZuiMlzgrJ7brNdPlkOXiX9x')
    messages = [
        {
                "role": "system",
                "content": "You are an expert Question Paper Generator, who is capable of generating MCQ Quiz Questions that strictly adhere to the context. The context is the syllabus for the subject."
        },
        {
            "role": "user",
            "content": f'''
                Generate for me a Question Paper that has a balance of Application-based and reasoning questions, within the context provided. Read, understand and reason with all the resources provided.
                Syllabus for the subject - {syllabus}

                You must generate {number_of_questions} MCQ Questions, strictly within the context of {modules_list}. Since the syllabus provided is a json string, each document is a module. Read and comprehend the following modules - {modules_list}.
                Each Multilple Choice Question must have 4 options, out of which only 1 must be right. Take care that all those 4 options must be relevant to the question asked, and must be strictly within then context.
                Strict care must be taken that there must be no spelling mistakes, and there must be no ambiguities while generating the questions.

                These {number_of_questions} questions must be in the following JSON format:
                [
                    Serial no : number,
                    Question : question,
                    Options : [
                        option1,
                        option2,
                        option3,
                        option4
                    ],
                    Answer : correct_option,
                    Module : module from which the question is fetched from
                ]

                If at all in the syllabus you see some algorithms that can be solved for, generate solving questions that forces the candidate to solve and find an answer using that particular algorithm or method.
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

    question_paper = chat_response.choices[0].message.content

    try:
        json_data = json.loads(question_paper)
        print("Corrected JSON data:")
        print(json.dumps(json_data, indent=4))
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    return json_data