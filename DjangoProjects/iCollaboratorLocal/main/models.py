from django.contrib.auth.models import User
from django.contrib.gis.db  import models
from datetime import datetime

class Course(models.Model):
    ID = models.IntegerField(max_length=6, primary_key=True)
    description = models.CharField(max_length=300, null=True)
    time = models.DateField(default=datetime.date(datetime.now()))
    objects = models.GeoManager()
    def __unicode__(self):
        return self.ID

class Session(models.Model):
    time = models.DateField(default=datetime.date(datetime.now()))
    location = models.PolygonField()
    course = models.ForeignKey('Course')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.time


class Student(models.Model):
    ID = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, unique = True)
    phone = models.IntegerField(max_length=11)
    courses = models.ManyToManyField('Course')
    sessions = models.ManyToManyField('Session')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    ID = models.IntegerField(max_length=4, primary_key=True)
    user = models.ForeignKey(User, unique = True)
    name = models.CharField(max_length=30, null=True)
    courses = models.ManyToManyField(to='Course')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Question(models.Model):
    question = models.CharField(max_length=300, null=True)
    right_answer = models.IntegerField(max_length=1, null=True)
    time = models.DateField(default=datetime.date(datetime.now()))
    answer1 = models.CharField(max_length=300, null=True)
    result1 = models.IntegerField(null=True)
    answer2 = models.CharField(max_length=300, null=True)
    result2 = models.IntegerField(null=True)
    answer3 = models.CharField(max_length=300, null=True)
    result3 = models.IntegerField(null=True)
    answer4 = models.CharField(max_length=300, null=True)
    result4 = models.IntegerField(null=True)
    session = models.ForeignKey('Session')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.question

class Notification(models.Model):
    content = models.CharField(max_length=300,null=True)
    time = models.DateField(default=datetime.date(datetime.now()))
    course = models.ForeignKey('Course')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.content

class Log(models.Model):
    content = models.CharField(max_length=300,null=True)
    time = models.DateField(default=datetime.date(datetime.now()))
    course = models.ForeignKey('Course')
    objects = models.GeoManager()

User.profile = property(lambda u: PubProfile.objects.get_or_create(user=u)[0])