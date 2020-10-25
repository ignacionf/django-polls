import os

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from polls.models import Question

class Command(BaseCommand):
    """Populate question db"""

    def handle(self, *args, **options):
        database = os.path.join(settings.BASE_DIR, 'data/questions.txt')
        try:
            for q in open(database, "r").readlines():
                Question(
                    question_text=q.rstrip(),
                    pub_date=timezone.now()).save()
        except KeyboardInterrupt:
            pass
