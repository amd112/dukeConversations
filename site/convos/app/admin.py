from django.contrib import admin
from .models import Student
from .models import Application
from .models import Professor
from .models import Attendance
from .models import Review
from .models import Dinner
# Register your models here.

admin.site.register(Student)
admin.site.register(Application)
admin.site.register(Professor)
admin.site.register(Attendance)
admin.site.register(Review)
admin.site.register(Dinner)