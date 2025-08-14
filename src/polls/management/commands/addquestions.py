from django.utils import timezone
import json
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from openai import OpenAI

from polls.models import Choice, Question


class Command(BaseCommand):
    help = 'Add questions to the database'

    def handle(self, *args, **options):
        pass
                

            

        









