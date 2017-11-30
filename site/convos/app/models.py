import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Student(models.Model):
	majors = ( 
		("1", "African and African American Studies"),
		("2", "Art History"),
		("3", "Asian and Middel Eastern Studies"),
		("4", "Biology"), 
		("5", "Biomedical Engineering"), 
		("6", "Biophysics"), 
		("7", "Brazilian and Global Portuguese Studies"), 
		("8", "Chemistry"), 
		("9", "Civil Engineering"), 
		("10", "Classical Civilization"), 
		("11", "Classical Languages"), 
		("12", "Computer Science"), 
		("13", "Cultural Anthropology"), 
		("14", "Dance"), 
		("15", "Earth and Ocean Sciences"), 
		("16", "Economics"), 
		("17", "Electrical and Computer Engineering"), 
		("18", "English"), 
		("19", "Environmental Engineering"), 
		("20", "Environmental Sciences"),
		("21", "Environmental Sciences and Policy"),
		("22", "Evolutionary Anthropology"), 
		("23", "French Studies"), 
		("24", "Gender, Sexuality, and Feminist Studies"), 
		("25", "German"), 
		("26", "Global Cultural Studies"), 
		("27", "Global Health"), 
		("28", "History"), 
		("29", "Interdepartmental Major"), 
		("30", "International Comparative Studies"), 
		("31", "Italian Studies"), 
		("32", "Linguistics"), 
		("33", "Mathematics"), 
		("34", "Mechanical Engineering"), 
		("35", "Medieval and Renaissance Studies"), 
		("36", "Music"), 
		("37", "Neuroscience"), 
		("38", "Philosophy"), 
		("39", "Physics"), 
		("40", "Political Science"), 
		("41", "Program II"), 
		("42", "Psychology"), 
		("43", "Public Policy Studies"), 
		("44", "Religious Studies"), 
		("45", "Romance Studies"), 
		("46", "Russian"), 
		("47", "Slavic and Eurasian Studies"), 
		("48", "Sociology"), 
		("49", "Spanish, Latin American, and Latino/a Studies"), 
		("50", "Statistical Science"),
		("51", "Theater Studies"), 
		("52", "Visual Arts"), 
		("53", "Visual and Media Studies"), 
		("54", "Undecided")
	)
	pronouns = (
		("1", "he/him/his"),
		("2", "she/her/hers"),
		("3", "they/them/theirs"),
		("4", "xe/xem/xyr"),
		("5", "other")
	)
	years = datetime.datetime.now().year
	years = range(years - 2, years + 5)
	years = [(str(x), str(x)) for x in years]
	username = models.CharField(max_length = 70, primary_key = True)
	id = models.CharField(max_length = 10, unique = True)
	name = models.CharField(max_length = 40)
	food_restrictions = models.CharField(max_length = 50, null = True, blank = True)
	netid = models.CharField(max_length = 7, unique = True)
	phone_number = models.IntegerField(unique = True)
	year = models.CharField(max_length = 1, choices = years)
	major = models. CharField(max_length = 1, choices = majors)
	pronoun = models.CharField(max_length = 1, choices = pronouns)
	def __str__(self):
		return self.username

class Professor(models.Model):
	genders = (
		("1", "M"),
		("2", "F"),
		("3", "O")
	)
	name = models.CharField(max_length = 40)
	food_restrictions = models.CharField(max_length = 50, null = True, blank = True)
	gender = models.CharField(max_length = 2, choices = genders)
	def __str__(self):
		return self.name
	
class Dinner(models.Model):
	date_time = models.DateTimeField(null = True)
	professor_id = models.ForeignKey(Professor, on_delete = models.DO_NOTHING)
	topic = models.CharField(max_length = 100)
	description = models.TextField(max_length = 1000)
	def __str__(self):
		return str(self.professor_id) + " on " + str(self.date_time.date())
	
class Application(models.Model):
	username = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	selected = models.NullBooleanField(default = None, null = True)
	date_time = models.DateTimeField(auto_now_add=True)
	interest = models.TextField(max_length = 1000)
	class Meta:
		unique_together = (("username", "dinner_id"),)
	def __str__(self):
		return str(self.username) + " for " + str(self.dinner_id)
		
class Review(models.Model):
	username = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	food_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)], null = True)
	convo_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)], null = True)
	food_comments = models.TextField(max_length = 1000, null = True)
	convo_comments = models.TextField(max_length = 1000, null = True)
	date_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		unique_together = (("username", "dinner_id"),)
	def __str__(self):
		return str(self.username) + " reviewed " + str(self.dinner_id)

class Attendance(models.Model):
	username = models.ForeignKey(Student, on_delete = models.DO_NOTHING, null = True)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING, null = True) 
	class Meta:
		unique_together = (("username", "dinner_id"),)
	def __str__(self):
		return str(self.username) + " attended " + str(self.dinner_id)
		
		
class Selection(Application):
    class Meta:
        proxy = True