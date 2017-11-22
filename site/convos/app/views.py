from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Application


def index(request):
	#latest_question_list = Application.objects.order_by('-date_time')[:5]
	#context = {'latest_question_list': latest_question_list}
	return render(request, 'html_work/homepage.html')
	
def loginhome(request):
	return(render(request, 'html_work/loginhome.html'))

def register(request):
	return render(request, 'html_work/signupdin.html')
	
def login(request):
	return render(request, 'html_work/login.html')
		
def signup(request):
	return render(request, 'html_work/register.html')
	
def confirm(request):
	return HttpResponse("You signed up for the thing!!")

def review(request):
	return render(request, 'html_work/reviewDinner.html')

def edit(request):
	return render(request, 'html_work/editprof.html')
	
#forgot password
#logged in mainpage?
#edit account