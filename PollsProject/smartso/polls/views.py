from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from forms import PollsForm,ChoiceForm
from django.forms import modelformset_factory


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
        model = Question
        template_name = 'polls/detail.html'
        def get_queryset(self):
            return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def create(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PollsForm(request.POST)
        cform=ChoiceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            # make changes to form fields before saving below
            
            # save form after changes to any form fields 
            instance.save()
            # return redirect ('polls:detail')
            # return HttpResponseRedirect(reverse('polls:results', args=(instance.id,)))
            return HttpResponseRedirect(reverse('polls:detail', args=[instance.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PollsForm()
        cform = ChoiceForm()
        # ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm)
        context ={
        "cform": cform,
        "form":form,
    }
    return render(request, 'polls/createpolls.html',context)