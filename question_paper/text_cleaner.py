# def cleaner(raw_text):
#     mcq_questions = []

#     questions = raw_text.split('\n\n')
#     # print(mcq_questions[0].split('\n'))
#     for i in questions:
#         # print(i.split('\n'))
#         lst = i.split('\n')
#         # print(lst)
#         mcq_questions.append({
#             'Question': lst[0],
#             'Options': [lst[1], lst[2], lst[3], lst[4]],
#             'Answer': lst[5][8:]
#         })

#     return mcq_questions

def cleaner(raw_text):
    mcq_questions = []
    
    # Split the raw text into questions, assuming each question is separated by double newlines
    questions = raw_text.split('\n\n')
    
    for i in questions:
        # Split each question into lines
        lst = i.split('\n')
        
        # Skip if there are fewer than 5 lines (in case the question doesn't have enough data)
        if len(lst) < 5:
            continue
        
        # Separate question text and options
        question_text = lst[0].strip()  # First line is the question
        options = [option.strip() for option in lst[1:5]]  # Next 4 lines are options
        
        # Extract the answer (assumes it starts with "Answer: ")
        answer_line = lst[5].strip()
        answer = answer_line[8:] if answer_line.startswith('Answer: ') else answer_line
        
        # Ensure that we always have 4 options
        while len(options) < 4:
            options.append("No option available")  # Fill with a default option if fewer than 4 options
        
        # Add the question as a dictionary to the result list
        mcq_questions.append({
            'Question': question_text,
            'Options': options,
            'Answer': answer
        })
    
    return mcq_questions
