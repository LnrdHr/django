from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    #question.choice_set is automatically created by Django when we define the ForeignKey in the Choice model(reversed relationship).
    #this allows us to access all choices related to a question instance
    #question.choice_set.all() will return all choices for that question
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text
