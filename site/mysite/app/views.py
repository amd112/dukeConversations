from django.shortcuts import render

# Create your views here.
def index(request):
	return HttpResponse("Hello world.")

def index(request, dinner_id):
	return HttpResponse("This is dinner %s" % dinner_id)
	return HttpResponse("This is dinner %s" % dinner_id)