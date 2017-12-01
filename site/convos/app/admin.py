from django.contrib import admin
from .models import Student, Application, Professor, Review, Dinner


# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('username', 'dinner_id', 'interest')
	list_display_links = ['username']
	list_per_page = 25

admin.site.register(Student)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Professor)
admin.site.register(Review)
admin.site.register(Dinner)
