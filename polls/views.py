from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import Question, Choice
from .handlers import handle_uploaded_file
from .strings import URLS, ERRORS

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, URLS.POLLS_INDEX, context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, URLS.POLLS_DETAIL, {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, URLS.POLLS_DETAIL, {
            'question': question,
            'error_message': ERRORS.NO_CHOICE,
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, URLS.POLLS_RESULTS, {'question': question})

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        return HttpResponseRedirect(URLS.POLLS_MAIN)
    else:
        form = UserCreationForm()
        return render(request, URLS.REGISTRATION, {
            'form': form,
        })

def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'], 'filename')
        return HttpResponseRedirect(URLS.UPLOAD_SUCCESS)
    else:
        form = UploadFileForm()
        return render(request, URLS.UPLOAD_PAGE, {'form': form})
