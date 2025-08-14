
import os
import sys
from django.apps import AppConfig
from django.utils import timezone
from django.core import management
from django.db.backends.signals import connection_created
from django.db.backends.postgresql.base import DatabaseWrapper
from django.dispatch import receiver



class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        import polls.signals

        if 'runserver' not in sys.argv: #avoid running during migrations or other management commands
            return

        if os.environ.get('RUN_MAIN') != 'true': #django auto-reloader runs this twice, once in the main process and once in the child process
            return
        
        

            
