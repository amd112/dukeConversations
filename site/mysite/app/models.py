from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
	id = models.CharField(max_length = 7, primary_key = True)
	name = models.CharField(max_length = 40)
	food_restrictions = models.CharField(max_length = 50)
	netid = models.CharField(max_length = 7, unique = True)
	phone_number = models.IntegerField(unique = True)
	year = models.IntegerField()
	major = models. CharField(max_length = 2, choices = majors)
	pronoun = models.CharField(max_length = 1, choices = pronouns)
	def __str__(self):
		return self.name

class Professor(models.Model):
	genders = (
		("1", "M"),
		("2", "F"),
		("3", "O")
	)
	name = models.CharField(max_length = 40)
	food_restrictions = models.CharField(max_length = 50)
	gender = models.CharField(max_length = 1, choices = genders)
	def __str__(self):
		return self.name
	
class Dinner(models.Model):
	date_time = models.DateTimeField(null = True)
	professor_id = models.ForeignKey(Professor, on_delete = models.DO_NOTHING)
	topic = models.CharField(max_length = 400)
	description = models.TextField(max_length = 1500)
	def __str__(self):
		return str(self.professor_id) + " at " + str(self.date_time)
	
class Application(models.Model):
	student_id = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	selected = models.NullBooleanField(default = None, null = True)
	date_time = models.DateTimeField()
	interest = models.TextField(max_length = 1000)
	class Meta:
		unique_together = (("student_id", "dinner_id"),)
	def __str__(self):
		return str(self.student_id) + " for " + str(self.dinner_id)
		
class Review(models.Model):
	student_id = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	food_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
	convo_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
	food_comments = models.TextField(max_length = 1000)
	convo_comments = models.TextField(max_length = 1000)
	date_time = models.DateTimeField()
	class Meta:
		unique_together = (("student_id", "dinner_id"),)
	def __str__(self):
		return str(self.student_id) + " reviewed " + str(self.dinner_id)

class Attendance(models.Model):
	student_id = models.ForeignKey(Student, on_delete = models.DO_NOTHING, null = True)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING, null = True) 
	class Meta:
		unique_together = (("student_id", "dinner_id"),)
	def __str__(self):
		return str(self.student_id) + " attended " + str(self.dinner_id)