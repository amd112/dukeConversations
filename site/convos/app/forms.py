from django import forms
from django.contrib.auth.models import User
from .models import Student

class loginForm(forms.Form):
	username = forms.CharField(max_length = 70)
	password = forms.CharField(max_length = 70)

class accountInfo(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('name', 'id', 'netid', 'phone_number', 'year', 'major', 'pronoun', 'food_restrictions')