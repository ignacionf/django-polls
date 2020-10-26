from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question
from .documents import QuestionDocument

from elasticsearch_dsl import Search

import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        q = self.request.GET.get("q", None)

        s = QuestionDocument.search()

        if q:
            s = s.query("match", text=q)

        qs = s.execute()

        return qs

def autocomplete(request):

    term = request.GET.get("term", None)
    options = {'term': term, 'options': []}

    if term:
        s = QuestionDocument.search()
        s = s.suggest("autocomplete", text=term, completion={"field": "suggest", "size": 20})
        data = s.execute().suggest.to_dict()

        for i in data['autocomplete'][0]['options']:
            options['options'].append(i['_source']['question_text'])

    return JsonResponse(options)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse(
            'polls:results',
            args=(question.id,)))
