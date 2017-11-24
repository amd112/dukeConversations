from django import forms
from django.contrib.auth.models import User
from .models import Student

class createAccount(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')

class accountInfo(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('name', 'id', 'netid', 'phone_number', 'year', 'major', 'pronoun', 'food_restrictions')