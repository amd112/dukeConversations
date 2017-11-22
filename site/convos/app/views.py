from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Application

# Create your views here.
def index(request):
	latest_question_list = Application.objects.order_by('-date_time')[:5]
	template = loader.get_template('index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))
	
def register(request):
	return HttpResponse("This is where you register for a dinner")
	
def login(request):
	return HttpResponse("This is where you login")
		
def signup(request):
	return HttpResponse("This is where you create an account")
	
def confirm(request):
	return HttpResponse("You signed up for the thing!!")

def review(request):
	return HttpResponse("This is where you review a dinner.")

#signup 
	#login
	#signup for dinner
	#signup confirmation
	#review a dinner
	#calendar?	