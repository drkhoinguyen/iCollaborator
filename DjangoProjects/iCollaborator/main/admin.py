__author__ = 'DUCMINHKHOI'
from django.contrib.gis import admin as geo_admin
from django.contrib import admin
from models import *

admin.site.register(Session)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Log)
admin.site.register(Question)
admin.site.register(Notification)
admin.site.register(Classroom, geo_admin.GeoModelAdmin)

