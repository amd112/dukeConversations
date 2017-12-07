from django.contrib import admin
from .models import Student, Application, Professor, Review, Dinner, Selection, Attendance

# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'interest')
	list_display_links = ['username']
	list_per_page = 25
	list_filter = ('dinner_id',)

class SelectionAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'interest', 'application_count', 'percent_selected', 'percent_attended', 'selected')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_filter = ('dinner_id',)
	list_editable = ('selected',)
	list_per_page = 15
	actions = ['download_csv']
	def download_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		from io import StringIO

		file = StringIO()
		writer = csv.writer(file)
		writer.writerow(['Username', 'Dinner ID', 'Interest', 'Application Count', 'Selection Percentage', 'Attendance Percentage', 'Selected'])
		for r in queryset:
			writer.writerow([r.username, r.dinner_id, r.interest, r.application_count, r.percent_selected, r.percent_attended, r.selected])

		file.seek(0)
		response = HttpResponse(file, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=selection_data.csv'
		return response

	download_csv.short_description = "Download a CSV File containing the selected rows"

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'attendance')
	search_fields = ('dinner_id__professor_id__name', 'dinner_id__date_time')
	list_filter = ('dinner_id',)
	list_editable = ('attendance',)
	list_per_page = 15

admin.site.register(Student)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Professor)
admin.site.register(Review)
admin.site.register(Dinner)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(Attendance, AttendanceAdmin)
