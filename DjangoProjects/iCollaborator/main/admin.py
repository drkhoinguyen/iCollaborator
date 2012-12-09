from django.contrib.admin.options import ModelAdmin
from form import *
import datetime

__author__ = 'DUCMINHKHOI'
from django.contrib.gis import admin as geo_admin
from django.contrib import admin
from models import *

class CourseAdmin(ModelAdmin):
    form = CourseForm2

class SessionAdmin(ModelAdmin):
    list_display = ['id','title', 'time', 'classroom', 'course']
    list_filter = ['classroom', 'course']
    search_fields = ['title', 'classroom', 'time', 'course']
    list_display_links = ['id', 'title']

class QuestionAdmin(ModelAdmin):
    list_display = ['question', 'right_answer', 'time', 'session']
    search_fields = ['question', 'right_answer', 'time', 'session']
    list_filter = ['session']

admin.site.register(Session, SessionAdmin)
admin.site.register(Teacher)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Notification)
admin.site.register(Classroom, geo_admin.GeoModelAdmin)

