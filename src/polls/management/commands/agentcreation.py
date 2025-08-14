from dotenv import load_dotenv
from mistralai import Mistral
from django.core.management.base import BaseCommand, CommandError


global mistral_client
global simple_agent

class Command(BaseCommand):
    help = "Create a Mistral agent"

    def handle(self, *args, **options):
        pass
    