from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iCollaborator.views.home', name='home'),
    # url(r'^iCollaborator/', include('iCollaborator.foo.urls')),

    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # url for students:
    url(r'^signup_stu/(?P<device_id>\w+)/(?P<student_name>\w+)/$', 'main.views.signup_stu'),
    url(r'^request_all_courses/(?P<device_id>\w+)/$', 'main.views.request_all_courses'),
    url(r'^request_course_info/(?P<device_id>\w+)/(?P<course_id>\w+)/$', 'main.views.request_course_info'),
    url(r'^request_nonce/(?P<device_id>\w+)/$', 'main.views.request_nonce_id'),
    url(r'^check_in/(?P<course_id>\w+)/(?P<output>\S+)', 'main.views.check_in_request'),
    url(r'^check_out/$', 'main.views.check_out'),
    url(r'^request_question/(?P<device_id>\w+)/(?P<course_id>\w+)/(?P<session_id>\w+)/$', 'main.views.request_question'),
    url(r'^answer_question/(?P<device_id>\w+)/(?P<course_id>\w+)/(?P<session_id>\w+)/(?P<question_id>\w+)/(?P<answer_id>\d+)/$',
                                                        'main.views.answer_question'),



    # url for normal user:
    url(r'^homepage/$', normal_homepage_view.as_view()),
    url(r'^aboutus/$', normal_about_us.as_view()),
    url(r'^login/$', 'main.views.login_view'),
    url(r'^signup/$', 'main.views.signup_view'),
    url(r'^success/$', 'main.views.success'),
    url(r'^unsuccess/$', 'main.views.unsuccess'),
    url(r'^test_connect/$', 'main.views.test_connect'),

    # url for login user:
    url(r'^login_homepage/$', 'main.views.homepage'),
    url(r'^login_aboutus/$', 'main.views.about_us'),
    url(r'^login_editaccount/$', 'main.views.edit_account'),
    url(r'^login_logout/$', 'main.views.logout_view'),
    url(r'^login_success/$', 'main.views.login_success'),

    # url for notification
    url(r'^login_notification/$', 'main.views.notification'),
    url(r'^login_notification/new_notification/$', 'main.views.new_notification'),
    url(r'^login_notification/(?P<note_id>\d+)/$', 'main.views.edit_notification'),

    # url for course
    url(r'^login_course/$', 'main.views.course'),
    url(r'^login_course/(?P<course_id>\d+)/show_statistic/$', 'main.views.show_course_statistic'),
    url(r'^login_course/(?P<course_id>\d+)/edit_course/$', 'main.views.edit_course'),

    # url for session
    url(r'^login_course/(?P<course_id>\d+)/session/$', 'main.views.session'),
    url(r'^login_course/(?P<course_id>\d+)/session/new_session/$', 'main.views.new_session'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/edit_session/$', 'main.views.edit_session'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/show_statistic/$', 'main.views.show_session_statistic'),

    # url for question
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/question/$', 'main.views.question'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/question/new_question/$', 'main.views.new_question'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/question/(?P<question_id>\d+)/edit_question/$', 'main.views.edit_question'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/question/(?P<question_id>\d+)/show_statistic/$', 'main.views.show_question_statistic'),
    url(r'^login_course/(?P<course_id>\d+)/session/(?P<session_id>\d+)/question/delete_question/$', 'main.views.delete_question'),

)

urlpatterns += staticfiles_urlpatterns()
