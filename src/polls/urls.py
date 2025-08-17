from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # Removed Django template URLs - using React frontend instead
    # path("",views.IndexView.as_view(), name="index"),
    # path("<int:pk>/",views.DetailView.as_view(), name="detail"),  
    # path("<int:pk>/results/",views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/",views.vote, name="vote"),
    
    # API endpoints for React frontend
    path("api/questions/", views.send_latest_questions_to_react, name="api_questions"),
    path("api/questions/<int:question_id>/", views.get_question_detail, name="api_question_detail"),
    path("api/questions/<int:question_id>/vote/", views.vote_api, name="api_vote"),
]