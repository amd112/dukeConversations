from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import send_mail


from django.template import RequestContext
from django.template.context_processors import csrf

from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_protect, csrf_exempt

import datetime
from .models import Application, Student, Dinner
from .forms import loginForm, accountInfo, registerDinner

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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
	if request.POST:
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
	if request.POST:
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			data = form.cleaned_data
			username = data['username']
			password = data['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return(redirect('edit'))
	else:
		form = UserCreationForm()
	return(render(request, 'html_work/register.html', {'form': form}))

@login_required(login_url = '/login')
#get the dinners they've applied to and upcoming dinners
#display status of their applications
def loginhome(request):
	startdate = datetime.date.today()
	enddate = startdate + datetime.timedelta(days=20)
	pastdate = startdate + datetime.timedelta(days=-20)
	future_dins = Dinner.objects.filter(date_time__range=[startdate, enddate])
	future_dins = future_dins.order_by('date_time')
	apps = Application.objects.filter(username = request.user.get_username())
	apps = apps.filter(date_time__range=[pastdate, startdate+datetime.timedelta(days=1)])
	apps = apps.order_by('-date_time')
	#still need to filter so the apps must equal one of the future dins
	context = {"dinners": future_dins, "applications":apps}
	return(render(request, 'html_work/loginhome.html', context))

@login_required(login_url = '/login')
def confirm(request):
	return render(request, 'html_work/confirm.html')
	
@login_required(login_url = '/login')
def confirm_review(request):
	return render(request, 'html_work/confirmreview.html')

@login_required(login_url = '/login')
@user_passes_test(check_complete_user, login_url='/edit')
def review(request):
	return render(request, 'html_work/reviewDinner.html')

@login_required(login_url = '/login')
#check if they already have a student object
#if they do, update info. If they don't, create
def edit(request):
	user = request.user.get_username()
	
	#see if they already have a student object entry
	#now when we reference we either edit existing, or create new
	try:
		student = Student.objects.get(username = user) 
	except ObjectDoesNotExist:
		student = None

	#if they entered data	
	if request.method == "POST": 
		form = accountInfo(request.POST, instance = student)
		form.fields['username'].widget.attrs['readonly'] = True
		if form.is_valid():
			form.save(commit=False)
			form.username = user
			#save their student object
			form.save()
			#get their email
			netid = form.cleaned_data['netid']
			email = netid + "@duke.edu"
			current = User.objects.get(username = user)
			current.email = email
			#save to their user obejct
			current.save()
			return redirect('/home')
	else:
		#build the form
		form = accountInfo(initial={'username':user}, instance=student)
		form.fields['username'].widget.attrs['readonly'] = True
	return render(request, 'html_work/editprof.html', {'form': form, "user": user})
	
@login_required(login_url = '/login')
@user_passes_test(check_complete_user, login_url='/edit')
#check they have reviewed all dinners before registering again
#doesn't pass the data to confirm correctly yet
def register(request):
	#get user object
	user = request.user.username
	user = Student.objects.get(username = user)
	
	#if they filled out form
	if request.POST:
		form = registerDinner(request.POST, user=user)
		if form.is_valid():
			data = form.cleaned_data
			#fill out automatic data
			din = data['dinner']
			din = Dinner.objects.get(pk = din)
			inter = data['interest']
			#save their application
			a = Application.objects.create(username = user, dinner_id = din, selected = None, interest = inter)
			a.save()
			return redirect('/confirm', {"user":user.username, "dinner":din.topic, "interest":inter})
	else:
		#show form
		form = registerDinner(user=user)
	return render(request, 'html_work/signupdin.html', {"form": form})
	
def password(request):
	return render(request, 'html_work/password.html')
#forgot password?
#password change?

def sendSimpleEmail(request):
	res=send_mail("hello world","how are you?", "noreply@Kimberly3.com", ["kne3@duke.edu"])
	return HttpResponse('%s'%res)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'html_work/change_password.html', {
        'form': form
    })