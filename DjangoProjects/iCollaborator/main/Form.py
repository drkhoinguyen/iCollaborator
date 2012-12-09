
__author__ = 'DUCMINHKHOI'
from django.forms import ModelForm
from main.models import *
from django import forms

from django.contrib.admin import widgets


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ('objects')

    def __init__(self,user,*args,**kwargs):
        super (NotificationForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['course'].queryset = Teacher.objects.filter(user__username = user)[0].courses.all()

class SessionForm(ModelForm):
    class Meta:
        model = Session
        exclude = ('objects', 'location')

    def __init__(self,user,*args,**kwargs):
        super (SessionForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['course'].queryset = Teacher.objects.filter(user__username = user)[0].courses.all()


class CourseForm(ModelForm):
    time = forms.CharField(label='Date Begin')
    class Meta:
        model = Course
        exclude = ('objects')

class CourseForm2(ModelForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)
    teachers = forms.ModelMultipleChoiceField(queryset=Teacher.objects.all(), required=False)
    class Meta:
        model = Course
        exclude = ('objects')

    def save(self, commit=True):
        instance = super(CourseForm2, self).save(commit=False)
        instance.save()
        for student in self.cleaned_data['students']:
            student.courses.add(instance)
            print("save student: " + student.name)
            student.save()

        for teacher in self.cleaned_data['teachers']:
            teacher.courses.add(instance)
            print("save student: " + teacher.name)
            teacher.save()

        return instance

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

    def __init__(self,course_id,*args,**kwargs):
        super (QuestionForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['session'].queryset = Session.objects.filter(course__ID = course_id)


    """ answer1 = forms.CharField(label='Choice 1')
    answer2 = forms.CharField(label='Choice 2')
    answer3 = forms.CharField(label='Choice 3')
    answer4 = forms.CharField(label='Choice 4')"""



