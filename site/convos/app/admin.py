from django.contrib import admin
from .models import Student, Application, Professor, Review, Dinner, Selection, Attendance


# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'interest')
	list_display_links = ['username']
	list_per_page = 25
	list_filter = ('dinner_id',)

class SelectionAdmin(admin.ModelAdmin):
	list_display = ('username', 'interest', 'selected')
	list_filter = ('dinner_id',)
	list_editable = ('selected',)
	list_per_page = 15

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('username','attendance')
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
