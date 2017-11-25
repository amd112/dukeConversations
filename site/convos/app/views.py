from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test


from django.template import RequestContext
from django.template.context_processors import csrf

from django.views.decorators.csrf import csrf_protect, csrf_exempt


from .models import Application, Student
from .forms import loginForm, accountInfo


def check_complete_user(user):
	return True

def index(request):
	#latest_question_list = Application.objects.order_by('-date_time')[:5]
	#context = {'latest_question_list': latest_question_list}
	return render(request, 'html_work/homepage.html')
	
#Works, but doesn't give incorrect password warning. 
#Uses form instead of ModelForm to feed data, checks w/ authenticate
@csrf_protect	
def log_in(request):
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			#gets here
			if user is not None:
				login(request, user)
				return(redirect('/home'))
	else:
		form = loginForm()
	return(render(request, 'html_work/login.html', {'form': form}))

#Works, seems to be appropriately linked everywhere
def log_out(request):
	logout(request)
	return(redirect('/'))

#Appears to work, don't touch
@csrf_protect	
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			#successfully creates user but authentication isn't working
			data = form.cleaned_data
			username = data['username']
			password = data['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				#got through the user is not None but login not working
				login(request, user)
				return(redirect('edit'))
	else:
		form = UserCreationForm()
	return(render(request, 'html_work/register.html', {'form': form}))

@login_required(login_url = '/login')
def loginhome(request):
	return(render(request, 'html_work/loginhome.html'))

@login_required(login_url = '/login')
def confirm(request):
	return HttpResponse("You signed up for the thing!!")

@login_required(login_url = '/login')
def review(request):
	return render(request, 'html_work/reviewDinner.html')

@login_required(login_url = '/login')
def edit(request):
	if request.method == 'POST':
		form = accountInfo(request.POST)
		if form.is_valid():
			username = request.user.username
			form.save(commit=False)
			form.username = username
			form.save()
	else:
		form = accountInfo()
	return render(request, 'html_work/editprof.html')

@login_required(login_url = '/login')
def register(request):
	#use check_complete_user to see if the person has completed form, pass to render. 
	#add to html so form is only rendered if their profile is complete
	return render(request, 'html_work/signupdin.html')
	
#forgot password
#logged in mainpage?
#password change