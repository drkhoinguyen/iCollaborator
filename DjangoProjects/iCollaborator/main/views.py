# Create your views here.
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView
from django.contrib.auth.forms import *
from main.form import *
from django.shortcuts import *
from django.contrib.auth.decorators import login_required

# def for normal homepage
class normal_homepage_view(TemplateView):
    template_name = "homepage.html"


class normal_about_us(TemplateView):
    template_name = "aboutus.html"


def login_view(request):
    #set functions of login here
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/login_homepage')
        else:
        # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass
    return render_to_response("login.html", {"authen_form": AuthenticationForm()},
            context_instance=RequestContext(request))

def signup_view(request):
    #set functions of sign up here, add is_staff = True
    return render_to_response("signup.html", {"createuser_form": UserCreationForm()},
        context_instance=RequestContext(request))

# def for login homepage
@login_required(login_url='/login')
def homepage(request):
    return render_to_response("login_homepage.html", {}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def about_us(request):
    return render_to_response("login_aboutus.html", {}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_account(request):
    #set functions of edit_account here
    return render_to_response("login_editaccount.html", {"passchange_form": PasswordChangeForm(request.user)},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect("/homepage")


# notification def
@login_required(login_url='/login')
def notification(request):
    #set functions of notification here
    notification_list = Notification.objects.all().order_by('-time')
    paginator = Paginator(notification_list, 1) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notifications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notifications = paginator.page(paginator.num_pages)

    return render_to_response("login_notification.html", {"notifications": notifications},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def new_notification(request):
    #add new notification
    new_notification_form = NotificationForm(initial={"course": Course.objects.all()});
    return render_to_response("login_notification_new.html", {"new_notification_form": new_notification_form},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_notification(request, note_id):
    note = Notification.objects.filter(id=note_id)[0]
    edit_notification_form = NotificationForm(instance=note)
    #add edit notification in here

    return render_to_response("login_notification_edit.html", {"edit_notification_form": edit_notification_form,
                                                               'note_id': note_id},
        context_instance=RequestContext(request))

# Course def
@login_required(login_url='/login')
def course(request):
    #set functions of course here
    course_list = Course.objects.all().order_by('-time')
    paginator = Paginator(course_list, 1) # Show 25 contacts per page

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
    top_student_miss = Student.objects.filter()
    top_session_student_miss = Session.objects.filter()
    student_miss_over = Student.objects.filter()
    return render_to_response("login_course_statistic.html", {"course_id": course_id,
                                                              "top_student_miss": top_student_miss,
                                                              "top_session_student_miss": top_session_student_miss,
                                                              "student_miss_over": student_miss_over},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_course(request, course_id):
    course = Course.objects.get(ID=course_id)
    edit_course_form = CourseForm(instance=course)
    return render_to_response("login_course_edit.html",
            {"course_id": course_id, 'edit_course_form': edit_course_form},
        context_instance=RequestContext(request))

# Session def
@login_required(login_url='/login')
def session(request, course_id):
    #set functions of session here
    session_list = Session.objects.all().order_by('time')
    paginator = Paginator(session_list, 1) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        sessions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sessions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sessions = paginator.page(paginator.num_pages)
    return render_to_response("login_session.html", {"sessions": sessions, "course_id": course_id},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def new_session(request, course_id):
    # add session here and automatically create new notification
    #add add notification
    add_session_form = SessionForm1(initial={"course": Course.objects.get(id=course_id)});
    return render_to_response("login_session_new.html", {"add_session_form": add_session_form,
                                                         "course_id": course_id},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def edit_session(request, course_id, session_id):
    # add session here and automatically create new notification
    session = Session.objects.get(id=session_id)
    edit_session_form = SessionForm(instance=session)
    return render_to_response("login_session_edit.html",
            {"edit_session_form": edit_session_form, "course_id": course_id,
             "session_id": session_id},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def show_session_statistic(request, course_id, session_id):
    date = Session.objects.get(id=session_id).time
    num_student_attend = 2 #change later
    num_question = 3 #change later
    top_tough_question = Question.objects.filter()
    top_easy_question = Question.objects.filter()
    avg_percent_right_answer = 1.2 #change later

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

# Question def
@login_required(login_url='/login')
def question(request, course_id, session_id):
    #set functions of question here
    question_list = Question.objects.all().order_by('-time')
    paginator = Paginator(question_list, 1) # Show 25 contacts per page

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
    add_question_form = QuestionForm1(initial={"session": Session.objects.get(id=session_id)});
    return render_to_response("login_question_new.html", {"add_question_form": add_question_form,
                                                          "course_id": course_id, "session_id": session_id},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_question(request, course_id, session_id, question_id):
    # add session here and automatically create new notification
    question = Question.objects.get(id=question_id)
    edit_question_form = QuestionForm(instance=question)
    return render_to_response("login_question_edit.html",
            {"edit_question_form": edit_question_form, "course_id": course_id,
             "session_id": session_id, "question_id": question_id},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def show_question_statistic(request, course_id, session_id, question_id):
    question = Question.objects.get(id=question_id)
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
                                                                "total_answer": total_answer},
        context_instance=RequestContext(request))

@login_required(login_url='/login')
def delete_question(request, course_id, session_id):
    pass

#Helper function
