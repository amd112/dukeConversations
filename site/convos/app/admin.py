from django.contrib import admin
from .models import Student, Application, Professor, Review, Dinner, Selection, Attendance

class ApplicationAdmin(admin.ModelAdmin):
	fields=('username','_name', '_year', '_major', 'dinner_id', 'interest', 'selected', 'attendance')
	list_display = ('_name', '_year', '_major', 'dinner_id', 'interest', 'selected', 'attendance')
	readonly_fields=('username', '_name', '_year', '_major', 'dinner_id', 'interest', 'selected', 'attendance')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_display_links = ['_name']
	list_per_page = 25
	list_filter = ('dinner_id',)
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Year', 'Major', 'Professor', 'Date', 'Interest', 'Selected', 'Attended'])
		for r in queryset:
			writer.writerow([r.username.name, r.username.get_year_display(), r.username.get_major_display(), r.dinner_id.professor_id.name, r.dinner_id.date_time, r.interest, r.selected, r.attendance])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=application_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

class SelectionAdmin(admin.ModelAdmin):
	fields=('username', '_year', '_major', 'dinner_id', 'interest', 'application_count', 'percent_selected', 'percent_attended', 'selected')
	list_display = ('username', '_year', '_major', 'dinner_id', 'interest', 'application_count', 'percent_selected', 'percent_attended', 'selected')
	readonly_fields=('username', '_year', '_major', 'dinner_id', 'interest', 'application_count', 'percent_selected', 'percent_attended', 'selected')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_filter = ('dinner_id',)
	#list_editable=('selected',)
	list_per_page = 15
	actions = ['download_csv', 'notify']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Year', 'Major', 'Professor', 'Date', 'Interest', 'Application Count', 'Selection Percentage', 'Attendance Percentage', 'Selected'])
		for r in queryset:
			writer.writerow([r.username.name, r.username.get_year_display(), r.username.get_major_display(), r.dinner_id.professor_id.name, r.dinner_id.date_time, r.interest, r.application_count, r.percent_selected, r.percent_attended, r.selected])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=selection_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

	def notify(self, request, queryset):
		from django.core.mail import send_mass_mail

		dinner = queryset[0].dinner_id

		queryset.update(selected=True)

		datalist = []

		for r in queryset:
			datalist.append(('Duke Conversations Dinner Selection', 'Congratulations! You have been selected to attend a dinner with ' + r.dinner_id.professor_id.name + ' scheduled for ' + r.dinner_id.date_time.strftime("%m/%d/%y") + '.', 'noreply@DukeConversation.com', [r.username.netid + '@duke.edu']))

		datatuple = tuple(datalist)

		rejected = Application.objects.filter(dinner_id=dinner, selected=None)

		rejected.update(selected=False) 

		rejected_list = []

		for r in rejected:
			rejected_list.append(('Duke Conversations Dinner Notification', 'Thank you for participating in the Duke Conversations program.\n Unfortunately, you have not been selected for the dinner with ' + r.dinner_id.professor_id.name + ' scheduled for ' + r.dinner_id.date_time.strftime("%m/%d/%y") + '.\n Check back with us soon for more faculty dinner opportunities!', 'noreply@DukeConversation.com', [r.username.netid + '@duke.edu']))

		datatuple = tuple(datalist)
		rejectiontuple = tuple(rejected_list)

		send_mass_mail(datatuple)
		send_mass_mail(rejectiontuple)
		return

	notify.short_description = "Select students for a dinner and notify them of their selection"

class AttendanceAdmin(admin.ModelAdmin):
	fields=('_name', '_pronouns', '_food_restrictions', '_phone_number', 'dinner_id', 'attendance')
	list_display = ('_name', '_pronouns', '_food_restrictions', '_phone_number', 'dinner_id', 'attendance')
	readonly_fields = ('username', '_name', '_pronouns', '_food_restrictions', '_phone_number', 'dinner_id', 'selected', 'interest')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_filter = ('dinner_id',)
	list_editable = ('attendance',)
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Pronouns', 'Food Restrictions', 'Phone Number', 'Professor', 'Date', 'Attended'])
		for r in queryset:
			writer.writerow([r.username.name, r.username.get_pronoun_display(), r.username.food_restrictions, r.username.phone_number, r.dinner_id.professor_id.name, r.dinner_id.date_time, r.attendance])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=attendance_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

class StudentAdmin(admin.ModelAdmin):
	fields=('name', 'pronoun', 'year', 'major', 'phone_number', 'username', 'unique_id', 'netid', 'food_restrictions')
	list_display=('name', 'year', 'major')
	readonly_fields=('name', 'pronoun', 'year', 'major', 'phone_number', 'username', 'unique_id', 'netid', 'food_restrictions')
	search_fields=('name', 'username', 'netid')
	list_filter = ('year', 'major')
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Pronouns', 'Year', 'Major', 'Phone Number', 'Username', 'UniqueID', 'NetID', 'Food Restrictions'])
		for r in queryset:
			writer.writerow([r.name, r.get_pronoun_display(), r.get_year_display(), r.get_major_display(), r.phone_number, r.username, r.unique_id, r.netid, r.food_restrictions])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=student_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"


class ProfessorAdmin(admin.ModelAdmin):
	fields=('name', 'gender', 'unique_id', 'food_restrictions')
	list_display=('name',)
	search_fields=('name', 'unique_id')
	list_filter=('gender',)
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Gender', 'UniqueID', 'Food Restrictions'])
		for r in queryset:
			writer.writerow([r.name, r.get_gender_display(), r.unique_id, r.food_restrictions])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=professor_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"


class ReviewAdmin(admin.ModelAdmin):
	fields=('username', '_name', 'dinner_id', 'food_grade', 'food_comments', 'convo_grade', 'convo_comments')
	list_display=('_name', 'dinner_id')
	readonly_fields=('username', '_name', 'dinner_id', 'food_grade', 'food_comments', 'convo_grade', 'convo_comments')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_filter=('dinner_id',)
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Name', 'Professor', 'Date', 'Food Grade', 'Food Comments', 'Conversation Grade', 'Conversation Comments'])
		for r in queryset:
			writer.writerow([r.username.name, r.dinner_id.professor_id.name, r.dinner_id.date_time, r.food_grade, r.food_comments, r.convo_grade, r.convo_comments])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=review_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

class DinnerAdmin(admin.ModelAdmin):
	fields=('professor_id', 'date_time', 'topic', 'description')
	list_display=('professor_id', 'date_time')
	search_fields = ('professor_id__name', 'date_time')
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Professor', 'Date', 'Topic', 'Description'])
		for r in queryset:
			writer.writerow([r.professor_id, r.date_time, r.topic, r.description])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=dinner_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Application, ApplicationAdmin)


