# Create your views here.
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView
from django.contrib.auth.forms import *
from main.form import *
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import datetime
from django.contrib.gis.geos import Point
from Crypto.Cipher import AES

# def for normal homepage
class normal_homepage_view(TemplateView):
    template_name = "homepage.html"


class normal_about_us(TemplateView):
    template_name = "aboutus.html"


def login_view(request):
    #set functions of login here
    error = "None"
    if request.method == "POST":
        error = "post method"
        form = AuthenticationForm(data=request.POST)
        error = form.is_valid()
        if form.is_valid():
            user = form.get_user()
            if form.clean() and user.is_active:
                if Teacher.objects.filter(user__username=user):
                    login(request, user)
                    return HttpResponseRedirect('/login_homepage')
                else:
                    return redirect('/unsuccess')
    else:
        # Return an 'invalid login' error message.
        form = AuthenticationForm()
        error = "not post method"
    return render_to_response("login.html", {"authen_form": form, "error": ""},
        context_instance=RequestContext(request))


def signup_view(request):
    #set functions of sign up here
    error = "begin"
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        error = form.is_valid()
        if form.is_valid():
            error = "form is valid"
            if form.clean_username() and form.clean_password2():
                error = None
                form.save()
                return redirect("/success")

    else:
        form = UserCreationForm()

    return render_to_response("signup.html", {"createuser_form": form, "error": error},
        context_instance=RequestContext(request))


def success(request):
    return render_to_response("success.html", context_instance=RequestContext(request))


def unsuccess(request):
    return render_to_response("unsuccess.html", context_instance=RequestContext(request))


# def for login homepage
@login_required(login_url='/login')
def login_success(request):
    return render_to_response("login_success.html", {}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def homepage(request):
    return render_to_response("login_homepage.html", {}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def about_us(request):
    return render_to_response("login_aboutus.html", {}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_account(request):
    #set functions of edit_account here
    error = "begin"
    if request.method == "POST":
        form = PasswordChangeForm(request.user, data=request.POST)
        error = form.is_valid()
        if form.is_valid():
            error = "form is valid"
            if form.clean_old_password() and form.clean_new_password2():
                form.save()
                error = None
                return redirect("/login_success")

    else:
        form = PasswordChangeForm(request.user)
    return render_to_response("login_editaccount.html", {"passchange_form": form, "error": ""},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect("/homepage")


# notification def
@login_required(login_url='/login')
def notification(request):
    #set functions of notification here
    courses = Teacher.objects.filter(user__username = request.user)[0].courses.all()
    notification_list = Notification.objects.filter(course__in=courses).order_by('-time')
    paginator = Paginator(notification_list, 25) # Show 25 contacts per page

    error = None
    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notifications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notifications = paginator.page(paginator.num_pages)

    return render_to_response("login_notification.html", {"notifications": notifications, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def new_notification(request):
    #add new notification
    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = NotificationForm(request.user, request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "Successfully Add new Notification"
                form.save()
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = NotificationForm(request.user)

    return render_to_response("login_notification_new.html", {"new_notification_form": form, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_notification(request, note_id):
    note = Notification.objects.get(id=note_id)
    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = NotificationForm(request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "Successfully Edit Notification"
                form.save()
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = NotificationForm(request.user, instance=note)

    return render_to_response("login_notification_edit.html", {"edit_notification_form": form,
                                                               'note_id': note_id, "error": error},
        context_instance=RequestContext(request))

# Course def
@login_required(login_url='/login')
def course(request):
    #set functions of course here
    course_list = Teacher.objects.filter(user__username = request.user)[0].courses.all().order_by('-time')
    paginator = Paginator(course_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        courses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        courses = paginator.page(paginator.num_pages)
    return render_to_response("login_course.html", {"courses": courses}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def show_course_statistic(request, course_id):

    courses = Course.objects.filter(ID = course_id)
    if len(courses) is not 0:

        now = datetime.datetime.now()
        sessions = Session.objects.filter(course__ID = course_id, time__lte=now)
        students = Student.objects.all()

        list_student = []
        for student in students:
            list_student.append(student)

        top_student_miss = []
        max_bound = min(len(students), 10)
        for i in range(0, max_bound):
            min1 = 100000
            min_value = None
            for student in list_student:
                number = len(set(student.sessions.all()).intersection(set(sessions)))
                if number < min1:
                    min1 = number
                    min_value = student
            if min_value is not None:
                top_student_miss.append(min_value)
                list_student.remove(min_value)

        list_session = []
        for session in sessions:
            list_session.append(session)

        top_session_student_miss =[]
        for i in range(0, max_bound):
            min1 = 100000
            min_value = None
            for session in list_session:
                number = len(session.student_set.all())
                if number < min1:
                    min1 = number
                    min_value = session
            if min_value is not None:
                top_session_student_miss.append(min_value)
                list_session.remove(min_value)

        student_miss_over = []
        for student in students:
            if len(sessions)-len(student.sessions.all()) > 3:
                student_miss_over.append(student)

        return render_to_response("login_course_statistic.html", {"course_id": course_id,
                                                                  "top_student_miss": top_student_miss,
                                                                  "top_session_student_miss": top_session_student_miss,
                                                                  "student_miss_over": student_miss_over},
            context_instance=RequestContext(request))
    else:
        error = "We don't have course you request or simultaneously corrupt by other thread"
        return render_to_response("login_course_statistic.html", {"error": error},
            context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_course(request, course_id):
    course = Course.objects.get(ID=course_id)
    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "form is clean"
                form.save()
                error = "Successfully Edit Course"
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = CourseForm(instance=course)

    return render_to_response("login_course_edit.html",
            {"course_id": course_id, 'edit_course_form': form, "error": error},
        context_instance=RequestContext(request))

# Session def
@login_required(login_url='/login')
def session(request, course_id):
    #set functions of session here
    session_list = Session.objects.filter(course__ID= course_id).order_by('time')
    paginator = Paginator(session_list, 25) # Show 25 contacts per page

    error = None
    page = request.GET.get('page')
    try:
        sessions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sessions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sessions = paginator.page(paginator.num_pages)
    return render_to_response("login_session.html", {"sessions": sessions, "course_id": course_id, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def new_session(request, course_id):
    # add session here and automatically create new notification
    #add add notification
    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = SessionForm(request.user, request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "form is clean"
                form.save()
                error = "Successfully Add New Session"
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = SessionForm(request.user, initial={"course": Course.objects.get(ID = course_id)})
    return render_to_response("login_session_new.html", {"add_session_form":form,
                                                         "course_id": course_id, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_session(request, course_id, session_id):
    # add session here and automatically create new notification
    session = Session.objects.get(id=session_id)
    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = SessionForm(request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "form is clean"
                form.save()
                error = "Successfully Edit Session"
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = SessionForm(request.user, instance=session)
    return render_to_response("login_session_edit.html",
            {"edit_session_form": form, "course_id": course_id,
             "session_id": session_id, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def show_session_statistic(request, course_id, session_id):
    sessions = Session.objects.filter(id=session_id)
    if len(sessions) is not 0:
        session = sessions[0]
        date = session.time
        num_student_attend = len(session.student_set.all()) #change later
        num_question = len(session.question_set.all()) #change later

        top_tough_question = []
        top_easy_question = []
        list_question = []
        for question in session.question_set.all():
            list_question.append(question)

        total_right_percent = 0
        max_bound = min(len(sessions), 3)
        for i in range(0, max_bound):
            min1 = 100000; max1 = -100000
            min_value = None; max_value = None
            for question in list_question:
                right_percent = 0.0
                total_answer = question.result1 + question.result2 + question.result3 + question.result4
                if total_answer is 0:
                    right_percent = 0.0
                elif question.right_answer == 1:
                    right_percent = question.result1 * 1.0 / total_answer * 100
                elif question.right_answer == 2:
                    right_percent = question.result2 * 1.0 / total_answer * 100
                elif question.right_answer == 3:
                    right_percent = question.result3 * 1.0 / total_answer * 100
                else:
                    right_percent = question.result4 * 1.0 / total_answer * 100

                if right_percent < min1:
                    min1 = right_percent
                    min_value = question

                if right_percent > max1:
                    max1 = right_percent
                    max_value = question

                if not i:
                    total_right_percent += right_percent

            if min_value is not None:
                top_tough_question.append(min_value)

            if max_value is not None:
                top_easy_question.append(max_value)
                list_question.remove(min_value)
                if max_value is not min_value:
                    list_question.remove(max_value)

        if num_question is not 0:
            avg_percent_right_answer = total_right_percent/num_question
        else:
            avg_percent_right_answer = 0

        return render_to_response("login_session_statistic.html", {"course_id": course_id,
                                                                   "session_id": session_id,
                                                                   "date": date,
                                                                   "num_student_attend": num_student_attend,
                                                                   "num_question": num_question,
                                                                   "top_easy_question": top_easy_question,
                                                                   "top_tough_question": top_tough_question,
                                                                   "avg_percent_right_answer": avg_percent_right_answer,
                                                                   },
                                    context_instance=RequestContext(request))

    else:
        error = "We don't have session you request or simultaneously corrupt by other thread"
        return render_to_response("login_session_statistic.html", {"error": error,
                                                                   },
            context_instance=RequestContext(request))


# Question def
@login_required(login_url='/login')
def question(request, course_id, session_id):
    #set functions of question here
    question_list = Question.objects.filter(session__id = session_id).order_by('-time')
    paginator = Paginator(question_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)
    return render_to_response("login_question.html", {"questions": questions, "course_id": course_id,
                                                      "session_id": session_id},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def new_question(request, course_id, session_id):
    error = "Begin"
    sessions = Session.objects.get(id=session_id)
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = QuestionForm(course_id, request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "form is clean"
                form.save()
                error = "Successfully Add New Question"
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = QuestionForm(course_id, initial={"session": Session.objects.get(id=session_id)});
    return render_to_response("login_question_new.html", {"add_question_form": form,
                                                          "course_id": course_id, "session_id": session_id,
                                                          "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_question(request, course_id, session_id, question_id):
    # add session here and automatically create new notification
    question = Question.objects.get(id=question_id)

    error = "Begin"
    #add edit notification in here
    if request.method == "POST":
        error = "POST"
        form = QuestionForm(course_id, request.POST)
        if form.is_valid():
            error = "Form is valid"
            if form.clean():
                error = "form is clean"
                form.save()
                error = "Successfully Edit Question"
            else:
                error = "have some error"
        else:
            error = "Form is not valid"
    else:
        error = None
        form = QuestionForm(course_id, instance=question)

    return render_to_response("login_question_edit.html",
            {"edit_question_form": form, "course_id": course_id,
             "session_id": session_id, "question_id": question_id, "error": error},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def show_question_statistic(request, course_id, session_id, question_id):
    questions = Question.objects.filter(id=question_id)
    if len(questions) is not 0:
        question = questions[0]
        total_answer = question.result1 + question.result2 + question.result3 + question.result4

        percentage1 = question.result1 * 1.0 / total_answer * 100
        percentage2 = question.result2 * 1.0 / total_answer * 100
        percentage3 = question.result3 * 1.0 / total_answer * 100
        percentage4 = question.result4 * 1.0 / total_answer * 100

        return render_to_response("login_question_statistic.html", {"course_id": course_id, "session_id": session_id,
                                                                    "question_id": question_id, "question": question,
                                                                    "percentage1": percentage1,
                                                                    "percentage2": percentage2,
                                                                    "percentage3": percentage3,
                                                                    "percentage4": percentage4,
                                                                    "total_answer": total_answer,},
                                    context_instance=RequestContext(request))
    else:
        error = "We don't have question you request or simultaneously corrupt by other thread"
        return render_to_response("login_question_statistic.html", {"error": error},
            context_instance=RequestContext(request))



@login_required(login_url='/login')
def delete_question(request, course_id, session_id):
    for question_id in request.POST.getlist('choose_question'):
        question = Question.objects.filter(id = question_id)[0]
        question.delete()

    return HttpResponseRedirect('/login_course/'+course_id+'/session/'+session_id+'/question/')

#Functions for log in student
def signup_stu(request, device_id, student_name):
    result = []
    check_user = User.objects.filter(username=student_name)
    students = Student.objects.filter(ID = device_id)
    if len(device_id) is 4 and len(check_user) is 0 and len(student_name) > 0 and len(students) is 0:
    #change len(device_id) to 64bit in real project
        user = User.objects.create_user(username=student_name, email="abc@email.com", password=device_id)
        user.save()
        student = Student.objects.create(ID=device_id, name=student_name, user=user)
        student.save()
        result.append({"signal": "signup_stu_success"})
    else:
        result.append({"signal": "signup_stu_unsuccess"})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')


def request_all_courses(request, device_id):
    result = []
    students = Student.objects.filter(ID=device_id)
    if len(students) is not 0:
        courses = students[0].courses.all()

        if len(courses) is 0:
            result.append({"signal": "not_exist_device"})
        else:
            list_courses = []
            for course in courses:
                dict_course = dict()
                dict_course["course_id"] = course.ID
                dict_course["course_name"] = course.name
                list_courses.append(dict_course)

            result.append({"courses": list_courses})
    else:
        result.append({"signal": "not_exist_device"})
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')


def request_course_info(request, device_id, course_id):
    result = []
    students = Student.objects.filter(ID=device_id)
    courses = Course.objects.filter(ID = course_id)
    if len(students) and len(courses) is not 0:
        now = datetime.datetime.now()
        course = courses[0]
        sessions = Session.objects.filter(time__gte=now.date(), course__ID = course_id).order_by('time')
        if len(sessions) is not 0:
            klass = sessions[0].classroom
            locations = [
                {"point_id": 0, "coordX": klass.location[0][0][0], "coordY": klass.location[0][0][1]},
                {"point_id": 1, "coordX": klass.location[0][1][0], "coordY": klass.location[0][1][1]},
                {"point_id": 2, "coordX": klass.location[0][2][0], "coordY": klass.location[0][2][1]},
                {"point_id": 3, "coordX": klass.location[0][3][0], "coordY": klass.location[0][3][1]},
            ]

            teacher_names = []
            for teacher in course.teacher_set.all():
                teacher_name = dict()
                teacher_name['teacher_name'] = teacher.name
                teacher_names.append(teacher_name)

            notifications = []
            for notice in Notification.objects.filter(course=course).order_by('-time'):
                notification = dict()
                notification['notification_content'] = notice.content
                notification['notification_time'] = unicode(notice.time)
                notifications.append(notification)

            if course.time.month <= 6:
                course_time = "Spring " + str(course.time.year)
            else:
                course_time = "Fall " + str(course.time.year)

            result.append({"course_name": course.name,
                           "course_description": course.description,
                           "course_time": course_time,
                           "classroom_name": klass.name,
                           "classroom_locations": locations,
                           "teacher_name": teacher_names,
                           "notifications": notifications})
        else: #cannot access
            result.append({"signal": "cannot_access"})
    else: #cannot access
        result.append({"signal": "cannot_access"})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def check_in_request(request, course_id, output):
    result = []
    #decrypt output and get specific values:
    [device_id_value, x_coord_value, y_coord_value, nonce_id_value] = get_output(output)

    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes = 75)
    now2 = now - delta
    sessions = Session.objects.filter(time__lte=now, time__gte=now2, course__ID=course_id)
    students = Student.objects.filter(ID = device_id_value)

    print "device_id_value = " + device_id_value
    print "x_coord_value = " + x_coord_value
    print "y_coord_value = " + y_coord_value
    print "nonce_id_value = " + nonce_id_value
    print "students = " + str(students)
    print "sessions = " + str(sessions)

    if device_id_value is not "" and x_coord_value is not "" \
            and y_coord_value is not "" and nonce_id_value is not "" and sessions.exists() and students.exists():

        student = students[0]
        session = sessions[0]

        nonce_id = student.nonce_id
        after = get_key(device_id_value, nonce_id)

        pnt = Point(float(x_coord_value), float(y_coord_value), srid=32140)
        is_contains = session.classroom.location.contains(pnt)

        print "point = " + str(pnt)
        print "is_contains = " + str(is_contains)
        print "student = " + str(student)
        print "nonce_id = " + str(nonce_id)
        print "after = " + after.decode('base64')
        print "nonce_id_value = " + nonce_id_value.decode('base64')
        print "after == nonce_id_value = " + str(after.decode('base64') == nonce_id_value.decode('base64'))
        print "session = " + str(session)

        if students.exists() and nonce_id_value.decode('base64') == after.decode('base64') \
                    and is_contains and session is not None and session in student.sessions.all():

            student.sessions.add(session)
            student.nonce_id += 1
            student.save()
            result.append({"signal": "check_in_stu_success" })
        else:
            result.append({"signal": "check_in_stu_unsuccess" })
    else:
        result.append({"signal": "check_in_stu_unsuccess" })

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def check_out(request):
    result = []

    result.append({"signal": "check_out_success"})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def request_nonce_id(request, device_id):
    result = []
    students = Student.objects.filter(ID = device_id)
    if len(students) is not 0:
        nonce_id = students[0].nonce_id
        after = get_key(device_id, nonce_id)
        print "after in request_nonce_id = " + str(after)

        result.append({"nonce_id_encrypt": after})
    else:
        result.append({"signal": "request_nonce_id_unsuccess"})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def get_output(output):
    #decode base 64 to byte array
    output2 = output.decode('base64')
#    print "output2 = " + output2
    key='0123456789abcdef'
    crypt = AES.new(key, AES.MODE_ECB)

    output = crypt.decrypt(output2)


    """output = "device_id=" + android_device_id + "x_coord=" +
    locationX + "y_coord="+ locationY + "nonce_id="+ nonce_id """

    device_id_index = output.find("device_id=")
    x_coord_index = output.find("x_coord=")
    y_coord_index = output.find("y_coord=")
    nonce_id_index = output.find("nonce_id=")

    device_id_value = output[device_id_index + len("device_id="):x_coord_index]
    x_coord_value = output[x_coord_index + len("x_coord="): y_coord_index]
    y_coord_value = output[y_coord_index + len("y_coord="): nonce_id_index]
    nonce_id_value = output[nonce_id_index + len("nonce_id="):]

    return [device_id_value, x_coord_value, y_coord_value, nonce_id_value]

def get_key(device_id, nonce_id):
    string = str(device_id) + str(nonce_id)
    enc = string.zfill(16)

    key='0123456789abcdef'
    crypt = AES.new(key, AES.MODE_ECB)

    cipher = crypt.encrypt(enc)

    return cipher.encode('base64')

def request_question(request, device_id, course_id, session_id):
    result = []
    students = Student.objects.filter(ID=device_id)
    if len(students) is not 0:
        courses = students[0].courses.all()
        list_questions = []

        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes= 75)
        now2 = now - delta
        sessions = Session.objects.filter(time__lte=now, time__gte=now2, course__ID=course_id, id=session_id)

        print "questions: " + str(sessions[0].question_set.all())
        print "questions student answered:" + str(students[0].questions.all())

        if len(sessions) is not 0:
            for question in sessions[0].question_set.all():
                if question not in students[0].questions.all():
                    print "GO HERE"
                    dict_question = dict()
                    dict_question["question_id"] = question.id
                    dict_question["question"] = question.question
                    list_answers = []

                    answer = dict()
                    answer['id'] = 1
                    answer['content'] = question.answer1
                    list_answers.append(answer)

                    answer = dict()
                    answer['id'] = 2
                    answer['content'] = question.answer2
                    list_answers.append(answer)

                    answer = dict()
                    answer['id'] = 3
                    answer['content'] = question.answer3
                    list_answers.append(answer)

                    answer = dict()
                    answer['id'] = 4
                    answer['content'] = question.answer4
                    list_answers.append(answer)

                    dict_question["answers"] = list_answers
                    list_questions.append(dict_question)
                result.append({"questions": list_questions})
        else:
            result.append({"signal": "request_question_unsuccess"})
    else:
        result.append({"signal": "request_question_unsuccess"})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def answer_question(request, device_id, course_id, session_id, question_id, answer_id):
    result1 = []
    students =  Student.objects.filter(ID = device_id)
    courses = Course.objects.filter(ID = course_id)
    sessions = Session.objects.filter(id= session_id)
    questions = Question.objects.filter(id = question_id)

    if students.exists() and courses.exists() and sessions.exists() and questions.exists() \
        and courses[0] in students[0].courses.all() and sessions[0] in students[0].sessions.all() \
        and questions[0] not in students[0].questions.all() and questions[0].session == sessions[0] \
        and int(answer_id) in [1,2,3,4]:

        question = Question.objects.get(id=question_id)
        answer = int(answer_id)
        if answer is 1:
            result = int(question.result1)
            question.result1 = result + 1
        elif answer is 2:
            result = int(question.result2)
            question.result2 = result + 1
        elif answer is 3:
            result = int(question.result3)
            question.result3 = result + 1
        else:
            result = int(question.result4)
            question.result4 = result + 1

        question.save()
        students[0].questions.add(questions[0])

        result1.append({"signal": "answer_submit_success"})
    else:
        result1.append({"signal": "answer_submit_unsuccess"})

    return HttpResponse(simplejson.dumps(result1), mimetype='application/json')

def test_connect(request):
    result = []

    result.append({"user": request.user})

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')