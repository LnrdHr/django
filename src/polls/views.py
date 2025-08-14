from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from polls.mistral_setup import get_agent,get_client

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
    
# def chat_view(request, user_input):
#     agent = get_agent()
#     client = get_client()
#     response = client.beta.conversations.start(
#     agent_id=agent.id,
#     inputs=user_input,
#     #store=False
# )


