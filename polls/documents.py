from django_elasticsearch_dsl import Document, Index, fields, Completion
from elasticsearch_dsl import analyzer, token_filter
from django_elasticsearch_dsl.registries import registry

from .models import Question, Choice

ascii_fold = analyzer(
    "ascii_fold",
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)


@registry.register_document
class QuestionDocument(Document):

    choices = fields.ObjectField(properties={
        'text': fields.TextField(),
        'votes': fields.IntegerField(),
    })

    text = fields.TextField()

    suggest = fields.CompletionField(analyzer=ascii_fold)

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
        choices = instance.choice_set.all()
        return [{"text": x.choice_text, "votes": x.votes} for x in choices]

    def prepare_suggest(self, instance):
        return instance.question_text.split()

    def prepare_text(self, instance):
        text = [instance.question_text]
        text.extend([x.choice_text for x in instance.choice_set.all()])
        return " ".join(text)
