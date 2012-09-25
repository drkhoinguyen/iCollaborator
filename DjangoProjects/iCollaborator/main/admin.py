__author__ = 'DUCMINHKHOI'
from django.contrib.gis import admin as geo_admin
from django.contrib import admin
from models import *

admin.site.register(Session, geo_admin.GeoModelAdmin)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Log)
admin.site.register(Question)
admin.site.register(Notification)


