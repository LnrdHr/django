import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from polls.mistral_setup import get_agent,get_client
import json

#using django's amend views here
#we dont have to use this type of naming convention for the views, but it's a common practice

class IndexView(generic.ListView):
    template_name="polls/index.html"
    ''' -from docs
    for ListView, the automatically generated context variable is question_list.
    To override this we provide the context_object_name attribute, specifying that we want to use latest_question_list instead.
    If we didn't override the that attribute, we would have to have model = Question and the context variable would be question_list.
    '''
    context_object_name = "latest_question_list" 

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:10]

class DetailView(generic.DetailView):
    model = Question
    template_name="polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name="polls/results.html"
          

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        #redisplay the voting form
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1 #instructs the database to increment the number of votes for the selected choice
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# API endpoints for React frontend
def send_latest_questions_to_react(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:10]
    questions_data = [
        {
            "id": question.id,
            "question_text": question.question_text,
            "pub_date": question.pub_date.isoformat()
        }
        for question in latest_question_list
    ]
    return JsonResponse(questions_data, safe=False)

def get_question_detail(request, question_id):
    """API endpoint for getting question details with choices"""
    question = get_object_or_404(Question, pk=question_id)
    choices_data = [
        {
            "id": choice.id,
            "choice_text": choice.choice_text,
            "votes": choice.votes,
            "correct": choice.correct
        }
        for choice in question.choice_set.all()
    ]
    
    question_data = {
        "id": question.id,
        "question_text": question.question_text,
        "pub_date": question.pub_date.isoformat(),
        "choices": choices_data
    }
    
    return JsonResponse(question_data)

def vote_api(request, question_id):
    """API endpoint for voting"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        data = json.loads(request.body)
        choice_id = data.get('choice_id')
        
        if not choice_id:
            return JsonResponse({'error': 'No choice selected'}, status=400)
            
        selected_choice = question.choice_set.get(pk=choice_id)
    except (json.JSONDecodeError, KeyError, Choice.DoesNotExist):
        return JsonResponse({'error': 'Invalid choice selected'}, status=400)
    
    # Increment vote count
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    
    # Return updated question data for results view
    choices_data = [
        {
            "id": choice.id,
            "choice_text": choice.choice_text,
            "votes": choice.votes,
            "correct": choice.correct
        }
        for choice in question.choice_set.all()
    ]
    
    question_data = {
        "id": question.id,
        "question_text": question.question_text,
        "choices": choices_data,
        "voted_choice_id": selected_choice.id
    }
    
    return JsonResponse(question_data)
