# -*- coding: latin-1 -*-
from .forms import *
import datetime, logging
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from .models import Choice, Question, Token, Votes
from django.template import RequestContext

# initialise logger
logger = logging.getLogger('votey')

# Create your views here.

@csrf_protect
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form_token = form.cleaned_data['token']
			form_username=form.cleaned_data['username']
			form_password=form.cleaned_data['password1']
			form_email=form.cleaned_data['email'] 
			if Token.objects.filter(token = form_token):	
				t = Token.objects.filter(token = form_token)[0]
			else:
				return render(request, 'votes/register.html', {'form' : form, 'message': "Ihr Token existiert nicht. Bitte verwenden sie ein existentes Token.."})
			if t.used is False:
				user = User.objects.create_user(username=form_username,password=form_password,email= form_email)
				setattr(t, 'used', True)
				setattr(t, 'used_by', User.objects.get(pk=user.id))
				t.save()
				logger.info('(Konto ' + form_token + '): Erfolgreich registriert.')
				return HttpResponseRedirect('/register/success/')
			else:
                                return render(request, 'votes/register.html', {'form' : form, 'message': "Ihr Token wurde bereits zur Registrierung eines Nutzerkontos verwendet. Melden sie sich einfach an."})
	else:
		form = RegistrationForm()
		return render(request,'votes/register.html',{'form':form})
 
def register_success(request):
    return render_to_response(
    'votes/success.html',
    )

def home(request):
	context = {'user' : request.user}
	return render(request, 'index.html', context)

@login_required(login_url='/login/')
def log(request):
	context = {'user' : request.user}
	return render(request, 'votes/log.html', context)


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'login/'
    redirect_field_name = 'next'
    template_name = 'votes/index.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Question
    template_name = 'votes/detail.html'

def get_queryset(self):
	return Question.objects.filter(pub_date__lte=timezone.now())

@login_required(login_url='/login/')
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	votes_list = Votes.objects.filter(question=question)
	finished = question.pub_date + datetime.timedelta(days=question.duration)
	context = { 'question' : question, 'votes_list' : votes_list, 'finished' : finished }
	return render(request, 'votes/results.html', context)	

@login_required(login_url='/login/')
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(choice_text=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Back to voting form
		return render(request, 'votes/detail.html', { 'question': question, 'error_message': "Bitte geben sie eine Entscheidung ein.", })
	else:
		user_token = Token.objects.filter(used_by=request.user)[0]
		if Votes.objects.filter(token=user_token).filter(question = question):
			return render(request, 'votes/detail.html', { 'question': question, 'error_message': "Sie haben bereits abgestimmt. Warten sie auf das Ende der Abstimmung um das Ergebnis zu sehen.", })
		else:	
			Votes.objects.create(token=Token.objects.filter(used_by=request.user)[0], question=question)
			selected_choice.votes += 1
			selected_choice.save()
			logger.info('(Konto ' + user_token.token + '): Antrag Nr. ' + question_id + ' abgestimmt.')
			return HttpResponseRedirect(reverse('votes:results', args=(question_id,)))
