import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_unique_id(value):
	if len(value) != 7:
		raise ValidationError(
	('%(value)s is not 7 digits!'),
	params={'value':value}
	)

def validate_required(value):
	if len(value) == 0:
		raise ValidationError(
	('This field is required!')
	)
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

	username = models.CharField(max_length = 30, primary_key = True, validators=[validate_required])
	unique_id = models.CharField(max_length = 7, unique = True, validators=[validate_unique_id])
	name = models.CharField(max_length = 40, validators=[validate_required])
	food_restrictions = models.CharField(max_length = 50, null = True, blank = True)
	netid = models.CharField(max_length = 7, unique = True, validators=[RegexValidator(regex='^[a-zA-Z]+[0-9]+')])
	phone_number = models.CharField(unique = True, max_length = 10, validators=[validate_required])
	year = models.CharField(max_length = 4, choices = years, validators=[validate_required])
	major = models.CharField(max_length = 10, choices = majors, validators=[validate_required])
	pronoun = models.CharField(max_length = 1, choices = pronouns, validators=[validate_required])
	def __str__(self):
		return self.username

	@classmethod
	def StudentForUsername(self, username):
	    return Student.objects.get(username=username)

class Professor(models.Model):
	genders = (
		("1", "M"),
		("2", "F"),
		("3", "O")
	)
	unique_id = models.CharField(max_length = 7, primary_key = True)
	name = models.CharField(max_length = 40)
	food_restrictions = models.CharField(max_length = 50, null = True, blank = True)
	gender = models.CharField(max_length = 5, choices = genders)

	def __str__(self):
		return self.name

#Ensure that no past dinners can be created. Perhaps not ensure this at db level tho (so that tests can run)?
class Dinner(models.Model):
	date_time = models.DateTimeField(null = True)
	professor_id = models.ForeignKey(Professor, on_delete = models.DO_NOTHING)
	topic = models.CharField(max_length = 100)
	description = models.TextField(max_length = 2000)

	class Meta:
		unique_together  = (("date_time", "professor_id"))

	def __str__(self):
		return str(self.professor_id) + " on " + str(self.date_time.date())

# Need to ensure nothing funny happens: so nothing like someone not chosen for a dinner shows up as attended
# this is not possible in models though, need to ensure this check somewhere else.
class Application(models.Model):
	#THE USERNAME BELOW REQUIRES AN ACTUAL STUDENT OBJECT!
	username = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	selected = models.NullBooleanField(default = None, null = True)
	attendance = models.BooleanField(default = False)
	date_time = models.DateTimeField(auto_now_add=True)
	interest = models.TextField(max_length = 1000)
	class Meta:
		unique_together = (("username", "dinner_id"),)
	def __str__(self):
		return str(self.username) + " for " + str(self.dinner_id)

	def _name(self):
		return self.username.name

	def _food_restrictions(self):
		return self.username.food_restrictions

	def _phone_number(self):
		return self.username.phone_number

	def _pronouns(self):
		return self.username.get_pronoun_display()

	def _year(self):
		return self.username.get_year_display()

	def _major(self):
		return self.username.get_major_display()

#username is not actually username, it is a student instance, so we may want to correct these
class Review(models.Model):
	username = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
	dinner_id = models.ForeignKey(Dinner, on_delete = models.DO_NOTHING)
	food_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
	convo_grade = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
	food_comments = models.TextField(max_length = 1000, null = True, blank = True)
	convo_comments = models.TextField(max_length = 1000, null = True, blank = True)
	date_time = models.DateTimeField(auto_now_add=True)

	def _name(self):
		return self.username.name

	class Meta:
		unique_together = (("username", "dinner_id"),)
	def __str__(self):
		return str(self.username) + " reviewed " + str(self.dinner_id)

	@classmethod
	def available_reviews(self, user):
		return Application.objects.filter(username=Student.StudentForUsername(user)).filter(selected=True).filter(attendance=True).values('dinner_id')

class AttendanceManager(models.Manager):
	def get_queryset(self):
		return super(AttendanceManager, self).get_queryset().filter(selected=True)

class Attendance(Application):
	objects = AttendanceManager()
	class Meta:
		proxy=True
		verbose_name='Attendance'
		verbose_name_plural='Attendance'

class Selection(Application):
	def _get_applied(self):
		return Application.objects.filter(username=self.username).count()

	def _get_selected_percentage(self):
		times_selected = Application.objects.filter(username=self.username, selected=True).count()
		times_applied = self._get_applied()
		if times_applied != 0:
			percent = (times_selected/times_applied)
			fpercent = "{:.1%}".format(percent)
		else:
			fpercent = "N/A"
		return fpercent

	def _get_attendance_percentage(self):
		times_attended = Application.objects.filter(username=self.username, attendance=True).count()
		times_selected = Application.objects.filter(username=self.username, selected=True).count()
		if times_selected != 0:
			percent = (times_attended/times_selected)
			fpercent = "{:.1%}".format(percent)
		else:
			fpercent = "N/A"
		return fpercent

	application_count=property(_get_applied)
	percent_selected=property(_get_selected_percentage)
	percent_attended=property(_get_attendance_percentage)

	class Meta:
		proxy=True
		verbose_name='Selection'
		verbose_name_plural='Selection'
