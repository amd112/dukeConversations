from django.contrib import admin
from .models import Student, Application, Professor, Attendance, Review, Dinner, Selection

f
# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'interest')
	list_display_links = ['username']
	list_per_page = 25
	
@admin.register(Selection)
class Selection(ModelAdmin):
    change_list_template = 'admin/selection.html'
	
admin.site.register(Student)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Professor)
admin.site.register(Attendance)
admin.site.register(Review)
admin.site.register(Dinner)
