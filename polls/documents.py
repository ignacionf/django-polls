from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from .models import Question, Choice


@registry.register_document
class QuestionDocument(Document):

    choices = fields.ObjectField(properties={
        'text': fields.TextField(),
        'votes': fields.IntegerField(),
    })

    text = fields.TextField()

    class Django:
        model = Question
        fields = [
            'id',
            'question_text',
            'pub_date',
        ]

    class Index:
        name = "es-dsl-question"

    def prepare_choices(self, instance):
        return [{"text": x.choice_text, "votes": x.votes} for x in instance.choice_set.all()]

    def prepare_text(self, instance):
        text = [instance.question_text]
        text.extend([x.choice_text for x in instance.choice_set.all()])
        return " ".join(text)

