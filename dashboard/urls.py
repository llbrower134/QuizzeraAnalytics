from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name="login"),
    url(r'^index/$', views.IndexView.as_view(), name="index"),
    url(r'^profile/$', views.ProfileView.as_view(), name="profile"),
    #url(r'^profile/(?P<student_id>\d+)/$', views.ProfileView.as_view(), name="profile"),

    # Visual specific pages for testing
    url(r'^quizavg/$', views.QuizAvgView.as_view(), name="quizavg"),
    url(r'^quizattempts/$', views.QuizAttemptsView.as_view(), name="quizattempts"),
    url(r'^quiztime/$', views.QuizTimeView.as_view(), name="quiztime"),

    url(r'^blank/$', views.BlankView.as_view(), name="blank"),
    url(r'^flot/$', views.FlotView.as_view(), name="flot"),

]
