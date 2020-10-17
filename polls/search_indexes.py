from haystack import indexes
from polls.models import Question, Choice


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    question_text = indexes.CharField(model_attr='question_text')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
