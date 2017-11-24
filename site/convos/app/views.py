from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User

from .models import Application, Student
from .forms import createAccount


def index(request):
	#latest_question_list = Application.objects.order_by('-date_time')[:5]
	#context = {'latest_question_list': latest_question_list}
	return render(request, 'html_work/homepage.html')
	
def loginhome(request):
	return(render(request, 'html_work/loginhome.html'))

@csrf_protect	
def login(request):
	return(render(request, 'html_work/login.html'))

@csrf_protect	
def signup(request):
	if request.method == 'POST':
		form = createAccount(request.POST)
		if form.is_valid():
			form.save()
			return(redirect('edit'))
	else:
		form = createAccount()
	return(render(request, 'html_work/register.html', {'form': form}))

@login_required(login_url = '/login')
def confirm(request):
	return HttpResponse("You signed up for the thing!!")

@login_required
def review(request):
	return render(request, 'html_work/reviewDinner.html')

@login_required
def edit(request):
	return render(request, 'html_work/editprof.html')

@login_required
def register(request):
	return render(request, 'html_work/signupdin.html')
	
#forgot password
#logged in mainpage?
#password change