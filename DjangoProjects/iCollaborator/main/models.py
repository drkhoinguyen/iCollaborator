from django.contrib.auth.models import User
from django.contrib.gis.db  import models
from datetime import datetime

class Course(models.Model):
    ID = models.IntegerField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    time = models.DateField(default=datetime.date(datetime.now()))
    objects = models.GeoManager()
    def __unicode__(self):
        return self.name

class Session(models.Model):
    time = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length=100)
    classroom = models.ForeignKey('Classroom')
    course = models.ForeignKey('Course')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

class Classroom(models.Model):
    location = models.PolygonField()
    name = models.CharField(max_length=30)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Student(models.Model):
    ID = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, unique = True)
    courses = models.ManyToManyField('Course', blank=True, null=True)
    sessions = models.ManyToManyField('Session', blank=True, null=True)
    questions = models.ManyToManyField('Question', blank=True, null=True)
    nonce_id = models.IntegerField(default=0)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    ID = models.IntegerField(max_length=4, primary_key=True)
    user = models.ForeignKey(User, unique = True)
    name = models.CharField(max_length=30)
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
    question = models.TextField(max_length=300)
    right_answer = models.IntegerField(max_length=1, choices=RIGHT_ANSWER_CHOICES)
    time = models.DateField(default=datetime.date(datetime.now()))
    answer1 = models.TextField(max_length=300)
    result1 = models.IntegerField(default= 0)
    answer2 = models.TextField(max_length=300)
    result2 = models.IntegerField(default= 0)
    answer3 = models.TextField(max_length=300)
    result3 = models.IntegerField(default= 0)
    answer4 = models.TextField(max_length=300)
    result4 = models.IntegerField(default= 0)
    session = models.ForeignKey('Session')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.question

class Notification(models.Model):
    content = models.TextField(max_length=300)
    time = models.DateField(default=datetime.date(datetime.now()))
    course = models.ForeignKey('Course')
    objects = models.GeoManager()

    def __unicode__(self):
        return self.content

User.profile = property(lambda u: PubProfile.objects.get_or_create(user=u)[0])