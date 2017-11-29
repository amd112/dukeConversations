import datetime

from django import forms
from django.contrib.auth.models import User
from .models import Student, Dinner, Professor, Application

class loginForm(forms.Form):
	username = forms.CharField(max_length = 70)
	password = forms.CharField(widget=forms.PasswordInput())
	


class accountInfo(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('username', 'name', 'id', 'netid', 'phone_number', 'year', 'major', 'pronoun', 'food_restrictions')

class registerDinner(forms.Form):
	def __init__(self,*args,**kwargs):
		self.user = kwargs.pop('user',None)
		super(registerDinner, self).__init__(*args,**kwargs)
		
		startdate = datetime.date.today()
		enddate = startdate + datetime.timedelta(days=20)
	
		#selecting all the dinners that are in the future
		future_dins = Dinner.objects.filter(date_time__range=[startdate, enddate]).values()
	
		#selecting all the applications already submitted by person
		applied = Application.objects.filter(username = self.user.username)
		applied = applied.values_list("dinner_id", flat=True)
	
		#creating tuples for the options to show, for future dinners, excluding already applied to
		options = [(x['id'], Professor.objects.get(id = x['professor_id_id']).name + ", " + x['topic'] + ", " + str(x['date_time'].date())) for x in future_dins if x['id'] not in applied]
		options = sorted(options, key=lambda tup: tup[1].split(",")[2]) #sorting by soonest date
	
		self.fields['dinner'].choices = options
		#self.fields['interest'] = forms.CharField(widget=forms.Textarea)
	
	dinner = forms.ChoiceField()
	interest = forms.CharField(widget=forms.Textarea)