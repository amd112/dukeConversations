from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import send_mail

from django.conf import settings

from django.template import RequestContext
from django.template.context_processors import csrf
from django.template.loader import render_to_string

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives

from django.views.decorators.csrf import csrf_protect, csrf_exempt

import os
from datetime import timedelta
import datetime
from .models import Application, Student, Dinner, Review, Professor, Attendance
from .forms import loginForm, accountInfo, registerDinner, reviewDinner

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.utils.html import strip_tags

def check_complete_user(user):
	try:
		exists = Student.objects.get(pk = user.username)
		exists = True
	except ObjectDoesNotExist:
		exists = False
	return exists

def no_outstanding_reviews(user):
	try:
		attended_dinners = Attendance.objects.filter(username = username).values_list("dinner_id", flat=True)
		upcoming = Dinner.objects.filter(date_time__gt=today).values_list("id", flat=True)
		reviewed_dinners = Review.objects.filter(username = username).values_list("dinner_id", flat=True)
		available_reviews = [x for x in attended_dinners if x not in reviewed_dinners and x not in upcoming]
		if len(available_reviews) > 0:
			return False
	except ObjectDoesNotExist:
		return True
	return True


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
			if not user:
				messages.error(request, 'Username and/or password is incorrect')
				form = loginForm()
				return(render(request, 'html_work/login.html', {'form': form}))
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
	#getting dinners in near future
	today = datetime.date.today()
	future_dins = Dinner.objects.filter(date_time__range=[today + timedelta(days = 7), today + timedelta(days = 27)])
	future_dins = future_dins.order_by('date_time')

	#get the relevent professor objects
	profs = Professor.objects.filter(unique_id__in = future_dins.values('professor_id_id'))

	#get the dinners relevant to applications
	upcoming = Dinner.objects.filter(date_time__range=[today + timedelta(days = -1), today + timedelta(days = 27)])
	d_id = upcoming.values('id')

	#getting applications from dinner list
	apps = Application.objects.filter(username = request.user.get_username())
	apps = apps.filter(dinner_id__in = d_id)
	apps = apps.order_by('date_time')

	context = {"dinners": future_dins, "applications":apps, "profs":profs}
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
	#get user object
	today = datetime.date.today()
	username = request.user.username
	user = Student.objects.get(username = username)
	attended_dinners = Attendance.objects.filter(username = username).values_list("dinner_id", flat=True)
	upcoming = Dinner.objects.filter(date_time__gt=today).values_list("id", flat=True)
	reviewed_dinners = Review.objects.filter(username = username).values_list("dinner_id", flat=True)
	available_reviews = [x for x in attended_dinners if x not in reviewed_dinners and x not in upcoming]

	#if they filled out form
	if request.POST:
		form = reviewDinner(request.POST, user=user)
		if form.is_valid():
			data = form.cleaned_data
			#fill out automatic data
			din = data['dinner']
			din = Dinner.objects.get(pk = din)
			food_grade = data['food_grade']
			convo_grade = data['convo_grade']
			food_comments = data['food_comments']
			convo_comments = data['convo_comments']
			#save their review
			r = Review.objects.create(username = user, dinner_id = din, food_grade = food_grade, convo_grade = convo_grade, food_comments = food_comments, convo_comments = convo_comments)
			r.save()
			return redirect('/confirmr')
	else:
		#show form
		form = reviewDinner(user=user)
	return render(request, 'html_work/reviewDinner.html', {"form": form, "dinners": available_reviews})

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
#@user_passes_test(no_outstanding_reviews, login_url='/review')
def register(request):
	#get user object
	username = request.user.username
	user = Student.objects.get(username = username)
	startdate = datetime.date.today()
	enddate = startdate + datetime.timedelta(days=20)
	future_dins = Dinner.objects.filter(date_time__range=[startdate, enddate]).values_list("id", flat=True)
	#selecting all the applications already submitted by person
	applied = Application.objects.filter(username = username)
	applied = applied.values_list("dinner_id", flat=True)

	applicable = [x for x in future_dins if x not in applied]

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
			request.session['prof_application'] = din.professor_id.name
			request.session['topic_application'] = din.topic
			request.session['date_application'] = din.date_time.date().strftime('%m/%d/%Y')
			a.save()
			return redirect('/emailpage')
	else:
		#show form
		form = registerDinner(user=user)
	return render(request, 'html_work/signupdin.html', {"form": form, "applicable": applicable})

def send_email(request):
	#get the signup information
	prof = request.session['prof_application']
	topic = request.session['topic_application']
	date = request.session['date_application']

	#get the user information
	user = request.user.username
	user = User.objects.get(username = user)
	email = user.email
	subject = "Your Duke Conversations signup has been submitted!"

	html_content = render_to_string('html_work/confirmationemail.html', {'professor':prof, 'topic':topic, 'date':date})
	text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, 'dukeconversation@gmail.com', [email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

	return redirect('/confirm')


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
