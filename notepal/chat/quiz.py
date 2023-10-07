import openai

QUIZ = """"
When a user requests to be tested or quizzed, analyze both the question posed by the user. 
Utilize this information to formulate appropriate questions for assessing the user's knowledge. 
Determine the optimal number of questions to present and set the difficulty level of these questions based on the user's proficiency. 
Additionally, choose the appropriate question format based on the content: for theoretical questions, 
prompt the user to type out their answer, whereas for objective questions, provide multiple-choice options.
The output should only be in this JSON:
       {
           'question': A list of the formulated question for the user.
            'type_of_question': A list that indicates whether each question is theoretical ('theory') or objective ('objective').
            'options': A list (Only for objective questions): A list of multiple-choice options for the user to choose from else 0.
            'the_answer': A list of the correct answers
       }
for example 
'{
  "questions": ["Evaluate the arithmetic expression 9 / 3.", "Which arithmetic operator is used for multiplication?"],
  "type_of_question": ["theory", "objective"],
  "options": [[], ["+", "-", "*", "/"]],
  "the_answer": ["3", "*"]
}'

"""


# takes the users quiz regarding quiz processes it and returns a JSON
def quiz_notify(user_message: str):
    message = [
        {
            "role": "system",
            "content": QUIZ,
        },
        {
            "role": "user",
            "content": user_message
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7,
    )

    return response
