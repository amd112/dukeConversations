from django.shortcuts import render

# Create your views here.
def index(request):
	return HttpResponse("Hello world.")

#def register(request):
#	return HttpResponse("This is where you register")
	
#def login(request):
#	return HttpResponse("This is where you login")
		
#def signup(request):
#	return HttpResponse("This is where you signup")