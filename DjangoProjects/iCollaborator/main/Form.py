
__author__ = 'DUCMINHKHOI'
from django.forms import ModelForm
from main.models import *
from django import forms

from django.contrib.admin import widgets


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ('objects')

class SessionForm(ModelForm):
    class Meta:
        model = Session
        exclude = ('objects', 'location')

class SessionForm1(ModelForm):
    class Meta:
        model = Session
        exclude = ('objects', 'location', 'course')

class CourseForm(ModelForm):
    time = forms.CharField(label='Date Begin')
    class Meta:
        model = Course
        exclude = ('objects')

class QuestionForm(ModelForm):

    class Meta:
        numberOfColumns = 50
        numberOfRows = 2
        model = Question
        exclude = ('objects', 'result1', 'result2', 'result3', 'result4')
        widgets = {
            'answer1': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer2': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer3': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer4': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            }

    """ answer1 = forms.CharField(label='Choice 1')
    answer2 = forms.CharField(label='Choice 2')
    answer3 = forms.CharField(label='Choice 3')
    answer4 = forms.CharField(label='Choice 4')"""

class QuestionForm1(ModelForm):

    class Meta:
        numberOfColumns = 50
        numberOfRows = 2
        model = Question
        exclude = ('objects', 'result1', 'result2', 'result3', 'result4', 'session')
        widgets = {
            'answer1': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer2': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer3': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            'answer4': forms.Textarea(attrs={'rows': numberOfRows, 'cols':numberOfColumns}),
            }




