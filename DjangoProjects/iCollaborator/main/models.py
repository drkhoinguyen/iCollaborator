from django.contrib.auth.models import User
from django.contrib.gis.db  import models
from datetime import datetime

class Course(models.Model):
    ID = models.IntegerField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100, null= True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    time = models.DateField(default=datetime.date(datetime.now()),blank=True, null=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return self.name

class Session(models.Model):
    time = models.DateField(default=datetime.date(datetime.now()),blank=True, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    classroom = models.ForeignKey('Classroom', null=True, blank= True)
    course = models.ForeignKey('Course', null=True, blank= True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

class Classroom(models.Model):
    location = models.PolygonField()
    name = models.CharField(max_length=30, null = True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Student(models.Model):
    ID = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, unique = True)
    phone = models.IntegerField(max_length=11)
    courses = models.ManyToManyField('Course', blank=True, null=True)
    sessions = models.ManyToManyField('Session', blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    ID = models.IntegerField(max_length=4, primary_key=True)
    user = models.ForeignKey(User, unique = True)
    name = models.CharField(max_length=30, null=True, blank= True)
    courses = models.ManyToManyField(to='Course', blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Question(models.Model):
    RIGHT_ANSWER_CHOICES = (
        (1, 'Choice 1'),
        (2, 'Choice 2'),
        (3, 'Choice 3'),
        (4, 'Choice 4'),
    )
    question = models.TextField(max_length=300, null=True, blank=True)
    right_answer = models.IntegerField(max_length=1, choices=RIGHT_ANSWER_CHOICES, null=True, blank= True)
    time = models.DateField(default=datetime.date(datetime.now()),blank=True, null=True)
    answer1 = models.TextField(max_length=300, null=True, blank=True)
    result1 = models.IntegerField(null=True, blank=True)
    answer2 = models.TextField(max_length=300, null=True, blank=True)
    result2 = models.IntegerField(null=True, blank=True)
    answer3 = models.TextField(max_length=300, null=True, blank=True)
    result3 = models.IntegerField(null=True, blank=True)
    answer4 = models.TextField(max_length=300, null=True, blank=True)
    result4 = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey('Session', blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.question

class Notification(models.Model):
    content = models.TextField(max_length=300,null=True, blank=True)
    time = models.DateField(default=datetime.date(datetime.now()), null=True, blank=True)
    course = models.ForeignKey('Course', null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.content

class Log(models.Model):
    content = models.TextField(max_length=300,null=True, blank=True)
    time = models.DateField(default=datetime.date(datetime.now()), null=True, blank=True)
    course = models.ForeignKey('Course', blank=True, null=True)
    objects = models.GeoManager()
    def __unicode__(self):
        return self.content

User.profile = property(lambda u: PubProfile.objects.get_or_create(user=u)[0])