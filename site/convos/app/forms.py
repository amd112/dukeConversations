import datetime

from django import forms
from django.contrib.auth.models import User
from .models import Student, Dinner, Professor, Application

class loginForm(forms.Form):
	username = forms.CharField(max_length = 70, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
	


class accountInfo(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(accountInfo, self).__init__(*args, **kwargs)
		majors = Student._meta.get_field('major').choices
		pronouns = Student._meta.get_field('pronoun').choices
		years = Student._meta.get_field('year').choices
		self.fields['major'].choices = majors
		self.fields['pronoun'].choices = pronouns
		self.fields['year'].choices = years
		for field in self.fields: 
			self.fields[field].widget.attrs.update({'class' : 'form-control'})
			
	class Meta:
		model = Student
		fields = ('username', 'name', 'id', 'netid', 'phone_number', 'year', 'major', 'pronoun', 'food_restrictions')
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
			'id': forms.TextInput(attrs={'class': 'form-control'}),
            'netid': forms.TextInput(attrs={'class': 'form-control'}),
			'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
			#needs to not be text input
			'major': forms.Select(attrs={'class': 'form-control'}),
            'pronoun': forms.Select(attrs={'class': 'form-control'}),
			'food_restrictions': forms.TextInput(attrs={'class': 'form-control'})
		}
		labels = {
            'netid': 'NetID',
			'id': 'Unique ID'
        }
		

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
		self.fields['dinner'].widget.attrs.update({'class' : 'form-control'})
		self.fields['interest'].widget.attrs.update({'class' : 'form-control'})
	
	dinner = forms.ChoiceField()
	interest = forms.CharField(widget=forms.Textarea)