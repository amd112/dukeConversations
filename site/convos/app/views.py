from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test


from django.template import RequestContext
from django.template.context_processors import csrf

from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_protect, csrf_exempt

import datetime
from .models import Application, Student
from .forms import loginForm, accountInfo, registerDinner


def check_complete_user(user):
	try:
		exists = Student.objects.get(pk = user.username)
		exists = True
	except ObjectDoesNotExist:
		exists = False
	return exists

def index(request):
	#latest_question_list = Application.objects.order_by('-date_time')[:5]
	#context = {'latest_question_list': latest_question_list}
	return render(request, 'html_work/homepage.html')
	
#Works, but doesn't give 'incorrect password' warning. 
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
@user_passes_test(check_complete_user, login_url='/edit')
def review(request):
	return render(request, 'html_work/reviewDinner.html')

#Works, don't mess with
@login_required(login_url = '/login')
def edit(request):
	user = request.user.get_username()
	try:
		student = Student.objects.get(username = user) 
	except ObjectDoesNotExist:
		student = None

	if request.method == "POST":
		form = accountInfo(request.POST, instance = student)
		form.fields['username'].widget.attrs['readonly'] = True
		if form.is_valid():
			form.save(commit=False)
			form.username = user
			form.save()
			return redirect('/home')
	else:
		form = accountInfo(initial={'username':user}, instance=student)
		form.fields['username'].widget.attrs['readonly'] = True
	return render(request, 'html_work/editprof.html', {'form': form, "user": user})

#maybe check to see if they have reviewed all the dinners they've been to	
@login_required(login_url = '/login')
@user_passes_test(check_complete_user, login_url='/edit')
def register(request):
	user = request.user.username
	if request.method == 'POST':
		form = registerDinner(request.POST)
		if form.is_valid:
			data = form.cleaned_data
			din = data['dinner']
			inter = data['interest']
			time = datetime.datetime.now()
			a = Application.objects.create(username = user, dinner_id = din, selected = None, date_time = time, interest = inter)
			a.save()
			return redirect('/confirm')
	else:
		form = registerDinner(user)
	return render(request, 'html_work/signupdin.html', {'form': form})
#forgot password?
#password change?