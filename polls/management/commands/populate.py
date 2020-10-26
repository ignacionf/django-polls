import os

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from polls.models import Question, Choice

class Command(BaseCommand):
    """Populate question db"""

    def handle(self, *args, **options):
        database = os.path.join(settings.BASE_DIR, 'data/questions.txt')
        try:
            for q in open(database, "r").readlines():
                instance = Question(
                    question_text=q.rstrip(),
                    pub_date=timezone.now())
                instance.save()

                Choice(choice_text="Vote 1", question=instance).save()
                Choice(choice_text="Vote 2", question=instance).save()
                Choice(choice_text="Vote 3", question=instance).save()
        except KeyboardInterrupt:
            pass
