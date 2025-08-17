import json
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from django.db.backends.signals import connection_created
from django.core.cache import cache
from django.dispatch import receiver
from openai import OpenAI
from django.utils.timezone import now
from polls.models import Choice, Question
from polls.mistral_setup import create_agent
from polls.views import IndexView
from polls.chatbot import initialize_chatbot


CACHE_QUESTIONS_TIMEOUT = 60 * 10 # 10 minutes
CACHE_AGENT_TIMEOUT = 60 * 60 # 1 hour

@receiver(connection_created)
def clear_questions_in_db(sender, **kwargs): #i want to keep only 10 questions in the database
    for question in Question.objects.all():
        if question not in IndexView().get_queryset():
            try:
                question.delete()
            except Exception as e:
                print(f"Error deleting question {question.id}: {e}")

#signal that is sent after the database is loaded(doesn't matter if the migrations were applied or not)
@receiver(connection_created) 
def make_openai_request(sender, **kwargs):

    #if the last_api_call doesn't exist or is older than 10 minutes, make a new request
    if cache.get('api_cooldown_openai'): #cooldown is active, which means we can't make a new request
        return False
    
    try:
        # Load environment variables
        load_dotenv('.env')

        # Create client (will automatically use OPENAI_API_KEY from environment)
        client = OpenAI()

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": """
                    Generate 10 general questions about Poland.
                    For each question, provide a list of 4 possible answers, with one correct answer and three incorrect ones.
                    The response should be formatted as a list of dictionaries, where each dictionary contains a question,
                    a dictionary of possible answers where a key is the answer and value is a boolean that indicates if it's correct.
                    The response output should be easily readable and ready to use, without additional parsing.
                    Return ONLY a valid JSON array. Do not include any variable names, explanations, or code.
                    Format each question as:
                    {
                        "question": "Question text here?",
                        "answers": {
                            "Answer 1": true,
                            "Answer 2": false,
                            "Answer 3": false,
                            "Answer 4": false
                        }
                    }
                    Start your response with [ and end with ]. Nothing else.
                    """
                }
            ]
        )
        raw_data = response.output[0].content[0].text

        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            raise TypeError(f"Failed to parse JSON response: {e}")
            
        
        for question in data:
            q = Question(
                question_text=question['question'],
                pub_date=now()
            )
            q.save()

            for answer, is_correct in question['answers'].items(): #TODO do i have to use items() here?
                c = Choice(
                    question=q,
                    choice_text=answer,
                    correct=is_correct
                )
                c.save()

        cache.set('api_cooldown_openai', True, timeout=CACHE_QUESTIONS_TIMEOUT)
        print("Questions added successfully.")
    except Exception as e:
        print(f"Error during initial question population: {e}")


@receiver(connection_created)
def run_chatbot_initialization(sender, **kwargs):
    try:
        initialize_chatbot()
        print("Chatbot initialized successfully.")
    except Exception as e:
        print(f"Error during chatbot initialization inside the signals.py: {e}")
#agent is created after the starting the server and if the agent isn't already cached
# @receiver(connection_created)
# def make_mistral_request(sender, **kwargs):

#     if cache.get('api_cooldown_mistral'):
#         return False
#     try:
#         simple_agent = create_agent()
#         cache.set('api_cooldown_mistral', True, timeout=CACHE_AGENT_TIMEOUT)
#         print("Agent created successfully.")
#     except Exception as e:
#         print(f"Error during agent creation: {e}")